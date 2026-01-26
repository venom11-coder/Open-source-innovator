
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

# basic filename check (optional)
def is_csv(file_content: bytes, filename: str) -> bool:

    if filename and not filename.lower().endswith(".csv"):
        return False

    if not file_content or not file_content.strip():
        return False

    # decode safely
    try:
        text = file_content.decode("utf-8-sig")  # handles BOM too
    except UnicodeDecodeError:
        return False

    # try parsing as comma-separated CSV
    try:
        reader = csv.reader(io.StringIO(text))
        first_row = next(reader, None)
        if not first_row:
            return False

        # require at least 2 columns in first row
        if len(first_row) < 2:
            return False

        return True
    except Exception:
        return False

@app.get("/osf-whoami")
async def osf_whoami():
    headers = {"Authorization": f"Bearer {OSF_TOKEN}"}
    async with httpx.AsyncClient(timeout=30) as client:
        me = await client.get("https://api.osf.io/v2/users/me/", headers=headers)
        node = await client.get(f"https://api.osf.io/v2/nodes/{PROJECT_ID}/", headers=headers)
    return {"me_status": me.status_code, "me": me.text[:300], "node_status": node.status_code, "node": node.text[:300]}

@app.get("/osf-perms")
async def osf_perms():
    headers = {"Authorization": f"Bearer {OSF_TOKEN}"}
    async with httpx.AsyncClient(timeout=30) as client:
        contrib = await client.get(
            f"https://api.osf.io/v2/nodes/{PROJECT_ID}/contributors/",
            headers=headers,
        )
    return {"status": contrib.status_code, "body": contrib.text[:2000]}



@app.post("/upload-to-osf")
async def upload_csv_to_osf(
    file: UploadFile = File(...),
    job_id: str | None = Form(None),
):
    if not OSF_TOKEN or not PROJECT_ID:
        raise HTTPException(status_code=500, detail="Missing OSF_TOKEN or PROJECT_ID")

    csv_bytes = await file.read()
    if not csv_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # (optional) relax this validation; csv.Sniffer often fails on small csvs
    if not is_csv(csv_bytes, file.filename):
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid CSV")

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

    async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
        resp = await client.put(upload_url, content=csv_bytes, headers=headers)

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return {"ok": True, "uploaded_filename": filename}

