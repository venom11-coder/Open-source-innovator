import os
from datetime import datetime, timezone
import subprocess
import io
from urllib.request import urlopen
import httpx
import csv
from dotenv import load_dotenv
import urllib
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# initialises FastAPI
app = FastAPI()

# for accessing the variables in the .env file
load_dotenv()

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
def is_csv(file_content: bytes, filename: str) -> bool:
    # basic filename check (optional)
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


@app.post("/upload-to-osf")
async def upload_csv_to_osf(
    file: UploadFile = File(...),
    job_id: str | None = Form(None),
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

        if not is_csv(csv_bytes, file.filename):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid CSV")

        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.put(upload_url, content=csv_bytes, headers=headers)

        if resp.status_code >= 400:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        # ✅ NEW: parse OSF response to get the file page URL
        payload = resp.json()

        file_id_full = payload.get("data", {}).get("id", "")  # "osfstorage/69916..."
        file_id = file_id_full.split("/")[-1]                # "69916..."

        project_id = PROJECT_ID  # "Rcusy" in your case

        osf_file_page_url = f"https://osf.io/{project_id}/files/osfstorage/{file_id}/"

        
        print(f"File uploaded successfully. OSF file page URL: {osf_file_page_url}")
        print(f"Full OSF response payload: {payload}")
        print(f"Upload URL: {upload_url}")
        print(f"Filename: {filename}")
        print(f"Safe Filename: {safe_name}")
        print(f"Request Headers: {headers}")

        return JSONResponse({
    "ok": True,
    "uploaded_filename": filename,
    "osf_file_page_url": osf_file_page_url,
    "osf_file_id": file_id,
})

    

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))