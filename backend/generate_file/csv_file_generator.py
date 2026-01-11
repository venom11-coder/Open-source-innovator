import csv
from urllib.request import urlopen
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from model import Output_Csv
import uuid
import io


# initialises FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create-csv")
async def create_csv(request: Request):
    data = await request.json()

    job_id = str(uuid.uuid4())
    created_at = data["datetime"]
    combinations = data["combinations"]
    seconds = data["seconds"]

    try:
        buf = io.StringIO()
        w = csv.writer(buf)

        w.writerow(["job_id", job_id])
        w.writerow(["created_at", created_at])
        w.writerow(["seconds_to_generate", seconds])
        w.writerow([])
        w.writerow(["compound_number", "materials"])

        for row in combinations:
            compound_number = row.get("compound_number")
            materials = row.get("materials", [])
            w.writerow([compound_number, " | ".join(materials)])

        csv_bytes = buf.getvalue().encode("utf-8")
        filename = f"{job_id}.csv"

        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)