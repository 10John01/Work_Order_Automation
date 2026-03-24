# --- authenticate_asana_oauth.py ---
# Handles Asana authentication via OAuth & PAT fallback.

import os
import json
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "../config/asana_token.json")
TOKEN_URL = "https://app.asana.com/-/oauth_token"

# ✅ Load Asana Credentials
ASANA_PAT = os.getenv("ASANA_PAT")
ASANA_CLIENT_ID = os.getenv("ASANA_CLIENT_ID")
ASANA_CLIENT_SECRET = os.getenv("ASANA_CLIENT_SECRET")
IS_RENDER = os.getenv("RENDER", "false").lower() == "true"

def load_tokens():
    """Loads stored Asana OAuth tokens."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    return {}

def save_tokens(token_data):
    """Saves Asana OAuth tokens to file."""
    with open(TOKEN_FILE, "w") as file:
        json.dump(token_data, file, indent=4)
    print(f"✅ Asana OAuth tokens saved to {TOKEN_FILE}")

def refresh_access_token():
    """Refreshes Asana OAuth token or falls back to PAT."""
    if not IS_RENDER:
        print("🔹 Running Locally: Using Personal Access Token (PAT)")
        return ASANA_PAT
    
    tokens = load_tokens()
    refresh_token = tokens.get("refresh_token")
    
    if not refresh_token:
        print("❌ ERROR: No refresh_token found! Asana OAuth required.")
        return None

    response = requests.post(TOKEN_URL, data={
        "grant_type": "refresh_token",
        "client_id": ASANA_CLIENT_ID,
        "client_secret": ASANA_CLIENT_SECRET,
        "refresh_token": refresh_token,
    })
    response_data = response.json()

    if "error" in response_data:
        print(f"❌ ERROR: {response_data['error_description']}")
        return None
    
    save_tokens(response_data)
    return response_data["access_token"]

def authenticate():
    """Authenticates Asana API using OAuth and returns the access token."""
    print("🔍 Authenticating with Asana...")
    token = refresh_access_token()
    if token:
        print("✅ Asana Authentication Successful!")
        return token
    print("❌ Authentication Failed!")
    return None

# ✅ Test authentication when running the script
if __name__ == "__main__":
    authenticate()
