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

def find_last_balance(text, keywords):
    # 🧠 THE CA HACK: Look for the last number that has (Cr) or (Dr) next to it!
    # This completely ignores broken tables and just finds the final money amount.
    cr_dr_pattern = r"(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:\(Cr\)|\(Dr\)|Cr|Dr)"
    cr_dr_matches = re.findall(cr_dr_pattern, text, re.IGNORECASE)
    
    if cr_dr_matches:
        return float(cr_dr_matches[-1].replace(',', ''))
        
    # Fallback just in case
    for keyword in keywords:
        pattern = rf"{keyword}.*?(\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return float(matches[-1].replace(',', ''))
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
        
        text_lower = full_text.lower()
        
        # 🧠 THE UNIVERSAL ROUTER
        is_bank_statement = any(word in text_lower for word in ["ifsc", "account no", "account number", "statement of account", "details of statement"])
        is_payslip = any(word in text_lower for word in ["payslip", "pay slip", "gross salary", "net pay", "earnings"])

        if is_bank_statement and not is_payslip:
            balance = find_last_balance(full_text, ["Closing Balance", "Total Balance", "Available Balance", "Net Balance", "Ledger Balance", "Balance()", "Balance"])
            return {
                "status": "Success",
                "doc_type": "bank_statement",
                "balance": balance,
                "filename": file.filename
            }
            
        else:
            gross = extract_amount(full_text, ["Gross Earnings", "Gross Salary", "Gross Total Income", "Total Earnings"])
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
