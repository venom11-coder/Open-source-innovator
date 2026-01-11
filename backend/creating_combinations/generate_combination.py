import json
import csv
import time
import pickle
import itertools
from urllib.request import urlopen
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from fastapi.middleware.cors import CORSMiddleware
from model import Combinations




# initialises FastAPI
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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