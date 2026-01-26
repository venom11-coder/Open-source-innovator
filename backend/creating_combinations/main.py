
import time
import csv
import io
import urllib
import uuid
import itertools
from urllib.request import urlopen
from fastapi import FastAPI, Request,UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from datetime import datetime, timezone
from model_csv import Output_Csv
import httpx
from zoneinfo import ZoneInfo
from fastapi.middleware.cors import CORSMiddleware
from model import Combinations
from dotenv import load_dotenv
import os




# initialises FastAPI
app = FastAPI()

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
OSF_TOKEN = os.getenv("OSF_TOKEN")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # so React can read filename header
)

# Post method to generate combinations out of the input given by frontend
@app.post("/generate-combinations")
def generate_combinations(data: Combinations):
    try:
        start_time = time.time()

        current_time_utc = datetime.now(timezone.utc)
        eastern = current_time_utc.astimezone(ZoneInfo("America/Toronto"))
        formatted_time_est = eastern.strftime("%Y-%m-%d %I:%M %p %Z")

        items = data.items
        k = data.size

        # basic validation
        if k < 1:
            raise HTTPException(status_code=400, detail="size must be >= 1")
        if k > len(items):
            raise HTTPException(status_code=400, detail=f"size cannot be greater than number of items ({len(items)})")

        combos = []
        compound_number = 1

        for combo in itertools.combinations(items, k):
            combos.append({
                "compound_number": compound_number,
                "materials": list(combo),
            })
            compound_number += 1

        print(f"Generated {len(combos)} combinations in {time.time() - start_time:.4f}s at {formatted_time_est}")

        return {"status": "good", "combinations": combos, "generated_at": formatted_time_est}

    except HTTPException:
        # re-raise clean API errors
        raise
    except Exception as e:
        # unexpected errors
        return {"status": "error", "message": str(e)}
    
@app.post("/create-csv")
async def create_csv(payload: Output_Csv):
    try:
        buf = io.StringIO(newline="")
        w = csv.writer(buf)

        job_id = str(uuid.uuid4())
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        filename = f"{job_id}_{ts}.csv"

        w.writerow(["job_id", job_id])
        w.writerow(["size", payload.size])
        w.writerow(["items", " | ".join(payload.items)])
        w.writerow(["combos", payload.combos])
        w.writerow([])
        w.writerow(["index", "combination"])

        for i, combo in enumerate(payload.combinations, start=1):
            w.writerow([i, combo])

        csv_bytes = buf.getvalue().encode("utf-8")

        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    
    # returns the filename based on the job_id and current time
def make_filename(job_id :  str) -> str:

    

    name = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{job_id}_{name}.csv"

# verifies if the uploaded file is a CSV, by reading the content and verifying the format and extension
def is_csv(file_content, filename):
    """
    Verifies if the provided file content is in CSV format.

    Args:
        file_content: The content of the file as a string (or bytes).
        filename: The original name of the file (used for basic extension check
                  and better error messages).

    Returns:
        bool: True if the content is likely a CSV, False otherwise.
    """
    # Optional: Basic filename extension check as a first filter
    if filename and not filename.lower().endswith('.csv'):
        print(f"Info: Filename extension is not .csv: {filename}")
        # Could return False here, but we check content to be sure

    # Convert bytes to string if necessary, assuming a common encoding like utf-8
    # For more robust encoding detection, you might need the 'chardet' library
    if isinstance(file_content, bytes):
        try:
            file_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            print("Error: Could not decode file content as utf-8.")
            return False

    # Check for empty content
    if not file_content.strip():
        return False

    # Use csv.Sniffer to check the dialect
    try:
        # Sniffer needs a sample string to analyze
        sample = file_content[:2048] # Read a sample (e.g., first 2KB)
        dialect = csv.Sniffer().sniff(sample)

        # Optional: Further checks on the detected dialect might be performed
        # e.g., check for a reasonable delimiter, like ',' or ';'
        if dialect.delimiter not in [',', ';', '\t']:
             print(f"Info: Detected delimiter '{dialect.delimiter}' is unusual.")

        # Try to read a few rows to ensure it's parsable
        # Wrap content in StringIO to treat the string as a file
        f = io.StringIO(file_content)
        reader = csv.reader(f, dialect)
        try:
            for _ in range(5): # Check the first 5 rows
                next(reader)
        except StopIteration:
            pass # File has fewer than 5 rows, which is fine
        except Exception as e:
            print(f"Error: Could not read rows with the detected dialect: {e}")
            return False
        
        return True
    
    # If Sniffer raises an error, it's likely not a valid CSV format
    except csv.Error as e:
        print(f"Error: Content does not appear to be in CSV format. Details: {e}")
        return False
    
     # Catch any other potential errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


@app.post("/upload-to-osf")
async def upload_csv_to_osf(
    file: UploadFile = File(...),
    job_id: str | None = Form(None),
):
    print(f"Debug: upload-to-osf called. incoming filename={file.filename}")
    print("osf id:", PROJECT_ID)
    print("osf token set:", bool(OSF_TOKEN))

    try:
        if not OSF_TOKEN or not PROJECT_ID:
            raise HTTPException(status_code=500, detail="Missing OSF_TOKEN or PROJECT_ID")

        csv_bytes = await file.read()
        if not csv_bytes:
            raise HTTPException(status_code=400, detail="Empty file")

        # validate it's actually CSV
        if not is_csv(csv_bytes, file.filename):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid CSV")

        # ensure job_id always exists
        job_id = job_id or str(uuid.uuid4())
        filename = make_filename(job_id)
        safe_name = urllib.parse.quote(filename)

        upload_url = (
            f"https://files.osf.io/v1/resources/{PROJECT_ID}/providers/osfstorage/"
            f"?kind=file&name={safe_name}"
        )

        headers = {
            "Authorization": f"Bearer {OSF_TOKEN}",
            "Content-Type": "application/octet-stream",
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.put(upload_url, content=csv_bytes, headers=headers)

        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        return JSONResponse({"ok": True, "uploaded_filename": filename})

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

