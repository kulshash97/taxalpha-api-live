from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import io

app = FastAPI()

# Security Shield (Lets your app talk to the web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The Dashboard / Status Check
@app.get("/")
def home():
    return {"status": "TaxAlpha API is LIVE 🚀", "message": "The Brain is running 24/7."}

# The PDF Reading Engine
@app.post("/upload")
async def extract_bank_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf = pdfplumber.open(io.BytesIO(contents))
        
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        
        return {
            "filename": file.filename,
            "status": "Success",
            "message": "PDF analyzed successfully! Ready for TaxAlpha.",
            "pages_read": len(pdf.pages)
        }
    except Exception as e:
        return {"error": str(e)}