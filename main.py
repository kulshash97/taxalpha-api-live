from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from supabase import create_client, Client
import os

# ==========================================
# 1. THE ARCHITECT'S CONFIGURATION
# Paste your keys here to bring the monopoly online
# ==========================================

GEMINI_API_KEY = "AIzaSyDlXLSyalmR_m1Zvhact5JewVH_qXXOKs8"
SUPABASE_URL = "https://bvmnpkkjuydzckbkrbfo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ2bW5wa2l1eXpsemtjcmJma2ZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4OTU0MjAsImV4cCI6MjA5MTQ3MTQyMH0.cLKRJ1DwI8RPsb-vxYmTii49eFLYeaoy5FM9tzMMbf8"

# Initialize the AI Brain
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize the Secure Vault (Supabase)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 2. THE API ROUTER
# ==========================================

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
    return {"status": "TaxAlpha Core Engine: Online & Connected to Supabase"}

@app.post("/analyze-client")
async def analyze_client(client_data: str = Form(...)):
    
    # The Bain-Level Prompt
    prompt = f"""
    You are the core intelligence of TaxAlpha, a world-class financial advisory firm.
    Analyze the following client data and provide a 3-point actionable wealth strategy 
    and confirm which ITR form they need. Be concise, professional, and authoritative.
    
    Client Data: {client_data}
    """
    
    try:
        # 1. AI generates the strategy
        response = model.generate_content(prompt)
        ai_insight = response.text
        
        # 2. Supabase logs the event securely
        # (Assuming you create a table called 'audit_logs' later)
        try:
            supabase.table("audit_logs").insert({
                "action": "Client Data Analyzed",
                "status": "Success"
            }).execute()
        except Exception as db_error:
            print(f"Database log skipped (table not created yet): {db_error}")

        # 3. Return to the frontend
        return {
            "status": "success",
            "ai_analysis": ai_insight
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
