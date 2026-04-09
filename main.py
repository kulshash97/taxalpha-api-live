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
        # This looks for the keyword followed by a number (handles commas like 39,080)
        pattern = rf"{keyword}.*?(\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(',', ''))
    return 0

@app.get("/")
def home():
    return {"status": "TaxAlpha Brain is Online 🚀"}

@app.post("/upload")
async def extract_bank_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf = pdfplumber.open(io.BytesIO(contents))
        
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
        
        # SEARCHING FOR REAL VALUES IN YOUR PAYSLIPS
        gross_val = extract_amount(full_text, ["Gross Earnings", "Gross Salary", "Gross Total Income"])
        taxable_val = extract_amount(full_text, ["Net Taxable Income", "Total Taxable", "Net Pay"])
        
        # Simple CA logic: if gross is over 5L, suggest a 500 late fee for demo
        fee_val = 500 if gross_val > 500000 else 0

        return {
            "status": "Success",
            "gross": gross_val,
            "taxable": taxable_val,
            "fee": fee_val,
            "filename": file.filename
        }
    except Exception as e:
        return {"error": str(e)}
