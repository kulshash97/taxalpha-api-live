from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import io
import re
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 DATA EXTRACTION UTILITY
def extract_text_from_pdf(contents):
    doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# 📂 ITR-U JSON GENERATOR (AY 2025-26)
@app.post("/generate-itr-json")
async def generate_itr_json(data: dict = Body(...)):
    # Standard ITR-U markers for Updated Return u/s 139(8A)
    itr_json = {
        "ITR": {
            "ITR1": {
                "CreationInfo": {"SWVersionNo": "1.0", "SWCreatedDate": datetime.now().strftime("%Y-%m-%d")},
                "PersonalInfo": {
                    "PAN": data.get("pan"),
                    "FirstName": data.get("first_name"),
                    "LastName": data.get("last_name")
                },
                "FilingStatus": {
                    "ReturnFileSec": "21", # 139(8A)
                    "ReturnType": "U",
                    "ReasonForUpdating": "01"
                },
                "ScheduleS": {
                    "GrossSalary": data.get("gross_salary", 0),
                    "DeductionUnderSection16": 75000, # AY 25-26 New Regime
                    "NetSalary": max(0, data.get("gross_salary", 0) - 75000)
                },
                "ScheduleIT": {
                    "TaxPayment": {
                        "BSRCode": data.get("bsr"),
                        "DateOfDeposit": data.get("date"),
                        "ChallanSerialNo": data.get("serial"),
                        "Tax": data.get("challan_amount")
                    }
                },
                "SummaryTax": {
                    "Fee234F": data.get("late_fee", 0),
                    "TotalTaxPayable": 0,
                    "AmountPayable": 0
                }
            }
        }
    }
    return itr_json
