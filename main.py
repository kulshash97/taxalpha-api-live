from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "TaxAlpha Brain is Online"}

@app.post("/generate-itr-json")
async def generate_itr_json(data: dict = Body(...)):
    # Precise Math for Sushmita Srivastava
    gross_sal = 436273
    interest = 891
    total_inc = gross_sal + interest
    std_deduction = 75000 
    taxable_inc = total_inc - std_deduction

    # EXACT SCHEMA REPLICATION
    return {
        "ITR": {
            "ITR1": {
                "CreationInfo": {
                    "SWVersionNo": "R7",
                    "SWCreatedBy": "SW90002526",
                    "JSONCreatedBy": "SW90002526",
                    "JSONCreationDate": datetime.now().strftime("%Y-%m-%d"),
                    "IntermediaryCity": "Delhi",
                    "Digest": "meOJRp2ZG7Q/iEHUw5w91X6vjIytml+YkV0Q/0P4Y+E="
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
                        "CountryCode": "91",
                        "PinCode": 500065,
                        "MobileNo": 9398495076,
                        "EmailAddress": "SUSHMITA.TAX@GMAIL.COM"
                    },
                    "DOB": "1996-03-22",
                    "EmployerCategory": "OTH"
                },
                "FilingStatus": {
                    "ReturnFileSec": 21,
                    "OptOutNewTaxRegime": "N",
                    "ItrFilingDueDate": "2025-07-31",
                    "clauseiv7provisio139i": "N"
                },
                "PartA_139_8A": {
                    "Name": "SUSHMITA SRIVASTAVA",
                    "PAN": "IJBPS5080L",
                    "AssessmentYear": "2025",
                    "PreviouslyFiledForThisAY": "N",
                    "LaidOutIn_139_8A": "Y",
                    "ITRFormUpdatingInc": "ITR1",
                    "UpdatingInc": {"ReasonsForUpdatingIncDtls": [{"ReasonsForUpdatingIncome": "1"}]},
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
                    "NetSalary": gross_sal,
                    "DeductionUs16": std_deduction,
                    "DeductionUs16ia": std_deduction,
                    "IncomeFromSal": gross_sal - std_deduction,
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
                    "Place": "HYDERABAD "
                }
            }
        }
    }
