from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_amount(text, keywords):
    for keyword in keywords:
        pattern = rf"{keyword}.*?(\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(',', ''))
    return 0

def calculate_tax_new_regime(taxable_income):
    if taxable_income <= 400000: return 0
    elif taxable_income <= 800000: return (taxable_income - 400000) * 0.05
    elif taxable_income <= 1200000: return 20000 + (taxable_income - 800000) * 0.10
    elif taxable_income <= 1600000: return 60000 + (taxable_income - 1200000) * 0.15
    elif taxable_income <= 2000000: return 120000 + (taxable_income - 1600000) * 0.20
    else: return 200000 + (taxable_income - 2000000) * 0.30

@app.post("/upload")
async def process_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf = pdfplumber.open(io.BytesIO(contents))
        full_text = "".join([page.extract_text() for page in pdf.pages])
        
        # 🧠 THE BRAIN ROUTER: What kind of document is this?
        text_lower = full_text.lower()
        
        # SCENARIO 1: It's a Bank Statement
        if "statement of account" in text_lower or "closing balance" in text_lower or "ledger balance" in text_lower:
            balance = extract_amount(full_text, ["Closing Balance", "Ledger Balance", "Available Balance", "Total Balance"])
            return {
                "status": "Success",
                "doc_type": "bank_statement",
                "balance": balance,
                "filename": file.filename
            }
            
        # SCENARIO 2: It's a Payslip
        else:
            gross = extract_amount(full_text, ["Gross Earnings", "Gross Salary", "Gross Total Income"])
            standard_deduction = 75000
            taxable_income = max(0, gross - standard_deduction)
            tax_due = calculate_tax_new_regime(taxable_income)
            savings = 12500 if gross > 700000 else 0 

            return {
                "status": "Success",
                "doc_type": "payslip",
                "gross": gross,
                "taxable": taxable_income,
                "tax_due": tax_due,
                "savings": savings,
                "filename": file.filename
            }
            
    except Exception as e:
        return {"error": str(e)}
