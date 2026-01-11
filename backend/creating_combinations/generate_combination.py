import json
import csv
import time
import pickle
import itertools
from urllib.request import urlopen
from fastapi import FastAPI, Request, File, UploadFile, Form
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

 start_time = time.time()
 current_time_utc = datetime.now(timezone.utc)

# convert to Eastern Time (uses EDT/EST correctly)
 eastern = current_time_utc.astimezone(ZoneInfo("America/Toronto"))

 formatted_time_est = eastern.strftime("%Y-%m-%d %I:%M %p %Z")
 

 #list for holding the new compounds
 listOfCompoundCombinations = []
 items = data.items
 K = data.size
 compoundNumber = 1

 # generates k combinations and appends them into the list of compound combinations
 for combination in  itertools.combinations(items,K):
   listOfCompoundCombinations.append({
                 "compound_number": compoundNumber,
            "materials": list(combination)
   })
   compoundNumber += 1


# FOR DEBUGGING ONLY
 print(listOfCompoundCombinations)
 print("Time to generate materials of three compounds\n --- %s seconds ---" % (time.time() - start_time))

 return JSONResponse({"status": "good", "combinations": listOfCompoundCombinations })