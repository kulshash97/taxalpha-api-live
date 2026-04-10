from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# 🛡️ THE MONOPOLY SHIELD: Allows your Netlify site to talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "TaxAlpha Brain is LIVE and Awake"}

@app.post("/generate-itr-json")
async def generate_itr_json(data: dict = Body(...)):
    # Calculate Math for Sushmita
    gross_sal = data.get("gross_salary", 0)
    interest = data.get("interest", 0)
    # New Tax Regime Standard Deduction for AY 25-26
    taxable_inc = max(0, (gross_sal + interest) - 75000) 
    
    # Official ITR-1 Updated Return Schema (The one you provided)
    return {
        "ITR": {
            "ITR1": {
                "CreationInfo": {
                    "SWVersionNo": "R7",
                    "SWCreatedBy": "SW90002526",
                    "JSONCreatedBy": "SW90002526",
                    "JSONCreationDate": datetime.now().strftime("%Y-%m-%d"),
                    "IntermediaryCity": "Hyderabad"
                },
                "Form_ITR1": {
                    "FormName": "ITR-1",
                    "AssessmentYear": "2025",
                    "SchemaVer": "Ver1.0",
                    "FormVer": "Ver1.0"
                },
                "PersonalInfo": {
                    "AssesseeName": {
                        "FirstName": data.get("first_name"),
                        "SurNameOrOrgName": data.get("last_name")
                    },
                    "PAN": data.get("pan"),
                    "DOB": "1996-03-22",
                    "EmployerCategory": "OTH"
                },
                "FilingStatus": {
                    "ReturnFileSec": 21,
                    "OptOutNewTaxRegime": "N"
                },
                "PartA_139_8A": {
                    "Name": f"{data.get('first_name')} {data.get('last_name')}",
                    "PAN": data.get("pan"),
                    "AssessmentYear": "2025",
                    "PreviouslyFiledForThisAY": "N",
                    "LaidOutIn_139_8A": "Y",
                    "ITRFormUpdatingInc": "ITR1",
                    "UpdatedReturnDuringPeriod": "1"
                },
                "PartB-ATI": {
                    "HeadOfInc": {"Salaries": gross_sal, "IncomeFromOS": interest, "Total": gross_sal + interest},
                    "UpdatedTotInc": taxable_inc,
                    "AmtPayable": data.get("late_fee"),
                    "FeeIncUS234F": data.get("late_fee"),
                    "NetPayable": data.get("late_fee"),
                    "ScheduleIT1": {
                        "TaxPayment1": {
                            "ITTaxPayments": [{
                                "slno": 1,
                                "BSRCode": data.get("bsr"),
                                "DateDep": data.get("date"),
                                "SrlNoOfChaln": int(data.get("serial")),
                                "Amt": data.get("challan_amount")
                            }]
                        },
                        "Total": data.get("challan_amount")
                    }
                },
                "Verification": {
                    "Declaration": {
                        "AssesseeVerName": f"{data.get('first_name')} {data.get('last_name')}",
                        "AssesseeVerPAN": data.get("pan")
                    },
                    "Capacity": "S",
                    "Place": "HYDERABAD"
                }
            }
        }
    }
