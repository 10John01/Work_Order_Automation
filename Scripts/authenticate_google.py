# --- authenticate_google.py ---
# 🚀 Handles authentication for Google APIs (Drive & Sheets)

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")

def authenticate():
    """Authenticates with Google APIs and returns Drive & Sheets services."""
    if not GOOGLE_CREDENTIALS_PATH or not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        raise FileNotFoundError("❌ ERROR: Google Credentials file missing! Check .env.")

    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
    )

    drive_service = build("drive", "v3", credentials=credentials)
    sheets_service = build("sheets", "v4", credentials=credentials)
    
    print("✅ Google API authentication successful using Service Account!")
    return drive_service, sheets_service
