from fastapi import FastAPI, Body
from datetime import datetime

app = FastAPI()

@app.post("/generate-itr-json")
async def generate_itr_json(data: dict = Body(...)):
    # Calculate Math for Sushmita
    gross_sal = data.get("gross_salary", 0)
    interest = data.get("interest", 0)
    gti = gross_sal + interest - 75000 # Std Deduction
    
    # Official ITR-1 Updated Return Schema
    itr_json = {
        "ITR": {
            "ITR1": {
                "CreationInfo": {
                    "SWVersionNo": "R7",
                    "SWCreatedBy": "SW90002526",
                    "JSONCreatedBy": "SW90002526",
                    "JSONCreationDate": datetime.now().strftime("%Y-%m-%d"),
                    "IntermediaryCity": "Hyderabad",
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
                    "AssesseeName": {
                        "FirstName": data.get("first_name"),
                        "SurNameOrOrgName": data.get("last_name")
                    },
                    "PAN": data.get("pan"),
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
                    "ReturnFileSec": 21, # 139(8A)
                    "OptOutNewTaxRegime": "N",
                    "ItrFilingDueDate": "2025-07-31"
                },
                "PartA_139_8A": {
                    "Name": f"{data.get('first_name')} {data.get('last_name')}",
                    "PAN": data.get("pan"),
                    "AssessmentYear": "2025",
                    "PreviouslyFiledForThisAY": "N",
                    "LaidOutIn_139_8A": "Y",
                    "ITRFormUpdatingInc": "ITR1",
                    "UpdatingInc": {"ReasonsForUpdatingIncDtls": [{"ReasonsForUpdatingIncome": "1"}]},
                    "UpdatedReturnDuringPeriod": "1"
                },
                "PartB-ATI": {
                    "HeadOfInc": {"Salaries": gross_sal, "IncomeFromOS": interest, "Total": gross_sal + interest},
                    "UpdatedTotInc": gti,
                    "AmtPayable": data.get("late_fee"),
                    "FeeIncUS234F": data.get("late_fee"),
                    "AggrLiabilityNoRefund": data.get("late_fee"),
                    "NetPayable": data.get("late_fee"),
                    "TaxUS140B": data.get("late_fee"),
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
                "ITR1_IncomeDeductions": {
                    "GrossSalary": gross_sal,
                    "Salary": gross_sal,
                    "NetSalary": gross_sal,
                    "DeductionUs16": 75000,
                    "DeductionUs16ia": 75000,
                    "IncomeFromSal": gross_sal - 75000,
                    "IncomeOthSrc": interest,
                    "TotalIncome": gti
                },
                "ITR1_TaxComputation": {
                    "TotalTaxPayable": 0,
                    "Rebate87A": 0, # Since income is low
                    "LateFilingFee234F": data.get("late_fee"),
                    "TotTaxPlusIntrstPay": data.get("late_fee")
                },
                "TaxPaid": {
                    "TaxesPaid": {"TotalTaxesPaid": data.get("challan_amount")},
                    "BalTaxPayable": 0
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
    return itr_json
