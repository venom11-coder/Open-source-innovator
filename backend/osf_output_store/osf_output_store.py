import os
from datetime import datetime, timezone
import subprocess
from urllib.request import urlopen
import httpx
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


@app.post("/upload-to-osf")
async def upload_csv_to_osf(
    file: UploadFile = File(...),
    job_id: str | None = Form(None),  # optional: pass job_id from frontend
):
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

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.put(upload_url, content=csv_bytes, headers=headers)

    if resp.status_code >= 400:
        # If you want, return resp.text to see OSF's error message
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return JSONResponse({"ok": True, "uploaded_filename": filename})