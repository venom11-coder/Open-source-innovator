import os
from datetime import datetime, timezone
import subprocess
import io
from urllib.request import urlopen
import httpx
import csv
import urllib
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# initialises FastAPI
app = FastAPI()

PROJECT_ID = os.getenv("PROJECT_ID")
OSF_TOKEN = os.getenv("OSF_TOKEN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    job_id: str | None = Form(None),  # optional: pass job_id from frontend
):
    
    try:
     if not OSF_TOKEN or not PROJECT_ID:
        raise HTTPException(status_code=500, detail="Missing OSF_TOKEN or OSF_PROJECT_ID")

     csv_bytes = await file.read()
     if not csv_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

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

     is_csv_file = is_csv(csv_bytes,file.filename)

     # valides if file is a csv or not
     if not is_csv_file:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid CSV")
   
     async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.put(upload_url, content=csv_bytes, headers=headers)

     if resp.status_code >= 400:
        # If you want, return resp.text to see OSF's error message
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
     
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse({"ok": True, "uploaded_filename": filename})