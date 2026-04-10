from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# 🛡️ THE MONOPOLY SHIELD: This allows Netlify to talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all sites (Netlify, Localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "TaxAlpha Brain is LIVE", "target": "AY 2025-26 ITR-U"}

@app.post("/generate-itr-json")
async def generate_itr_json(data: dict = Body(...)):
    # Precise Math for Sushmita
    gross_sal = 436273
    interest = 891
    total_inc = gross_sal + interest
    taxable_inc = total_inc - 75000 # Standard Deduction

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
                    "Description": "For Indls having Income from Salary, Pension, family pension and Interest",
                    "AssessmentYear": "2025",
                    "SchemaVer": "Ver1.0",
                    "FormVer": "Ver1.0"
                },
                "PersonalInfo": {
                    "AssesseeName": {"FirstName": "SUSHMITA", "SurNameOrOrgName": "SRIVASTAVA"},
                    "PAN": "IJBPS5080L",
                    "Address": {
                        "ResidenceNo": "23-6-818/2",
                        "ResidenceName": "KHOVA BELA SHAH ALI BANDA",
                        "LocalityOrArea": "CHARMINAR",
                        "CityOrTownOrDistrict": "HYDERABAD",
                        "StateCode": "36",
                        "PinCode": 500065
                    },
                    "DOB": "1996-03-22",
                    "EmployerCategory": "OTH"
                },
                "FilingStatus": {
                    "ReturnFileSec": 21, # 139(8A) Updated Return
                    "OptOutNewTaxRegime": "N",
                    "ItrFilingDueDate": "2025-07-31"
                },
                "PartA_139_8A": {
                    "Name": "SUSHMITA SRIVASTAVA",
                    "PAN": "IJBPS5080L",
                    "AssessmentYear": "2025",
                    "PreviouslyFiledForThisAY": "N",
                    "LaidOutIn_139_8A": "Y",
                    "ITRFormUpdatingInc": "ITR1",
                    "UpdatedReturnDuringPeriod": "1"
                },
                "PartB-ATI": {
                    "HeadOfInc": {"Salaries": gross_sal, "IncomeFromOS": interest, "Total": total_inc},
                    "UpdatedTotInc": taxable_inc,
                    "AmtPayable": 1000,
                    "FeeIncUS234F": 1000,
                    "AggrLiabilityNoRefund": 1000,
                    "NetPayable": 1000,
                    "TaxUS140B": 1000,
                    "ScheduleIT1": {
                        "TaxPayment1": {
                            "ITTaxPayments": [{
                                "slno": 1,
                                "BSRCode": "0510002",
                                "DateDep": "2026-04-10",
                                "SrlNoOfChaln": 20662,
                                "Amt": 1000
                            }]
                        },
                        "Total": 1000
                    }
                },
                "ITR1_IncomeDeductions": {
                    "GrossSalary": gross_sal,
                    "Salary": gross_sal,
                    "DeductionUs16": 75000,
                    "NetSalary": gross_sal - 75000,
                    "IncomeFromSal": gross_sal - 75000,
                    "IncomeOthSrc": interest,
                    "TotalIncome": taxable_inc
                },
                "ITR1_TaxComputation": {
                    "TotalTaxPayable": 0,
                    "Rebate87A": 0,
                    "LateFilingFee234F": 1000,
                    "TotTaxPlusIntrstPay": 1000
                },
                "Verification": {
                    "Declaration": {
                        "AssesseeVerName": "SUSHMITA SRIVASTAVA",
                        "AssesseeVerPAN": "IJBPS5080L"
                    },
                    "Capacity": "S",
                    "Place": "HYDERABAD"
                }
            }
        }
    }
