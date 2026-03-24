# --- work_order_pdf_handler.py ---
# 🚀 This script exports a Google Sheets work order as a PDF, prints it, and stores it in Google Drive.

import os
import time
import requests
import subprocess
from googleapiclient.http import MediaFileUpload
from authenticate_google import authenticate
from dotenv import load_dotenv

# ✅ Load environment variables (Ensures correct API access)
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Retrieve Google Drive API service
drive_service, sheets_service = authenticate()

PARENT_FOLDER_ID = os.getenv("PARENT_FOLDER_ID")  # Root folder for storing PDFs

def export_work_order_to_pdf(spreadsheet_id, drive_service):
    """Exports a Google Sheets work order to a PDF format and stores it in Google Drive."""
    
    pdf_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=pdf"
    headers = {"Authorization": f"Bearer {os.getenv('GOOGLE_API_TOKEN')}"}

    try:
        response = requests.get(pdf_url, headers=headers)
        if response.status_code == 200:
            pdf_path = f"/tmp/Work_Order_{spreadsheet_id}.pdf"

            # ✅ Save the PDF locally before uploading
            with open(pdf_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Work Order exported as PDF: {pdf_path}")

            # ✅ Step 2: Upload PDF to Google Drive
            drive_pdf_id = upload_pdf_to_drive(pdf_path, drive_service)
            if not drive_pdf_id:
                print(f"❌ ERROR: Failed to upload PDF for {spreadsheet_id}")
                return None

            # ✅ Step 3: Send the PDF to the printer
            if not send_to_printer(pdf_path):
                print(f"❌ ERROR: Failed to print {pdf_path}")

            return pdf_path
        
        else:
            print(f"❌ ERROR: Failed to export Work Order {spreadsheet_id} to PDF: {response.text}")
            return None

    except Exception as e:
        print(f"❌ ERROR: Failed to export Work Order {spreadsheet_id} to PDF: {e}")
        return None

def upload_pdf_to_drive(pdf_path, drive_service):
    """Uploads the generated PDF to Google Drive."""
    
    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: PDF file {pdf_path} does not exist.")
        return None

    try:
        file_metadata = {
            "name": os.path.basename(pdf_path),
            "parents": [PARENT_FOLDER_ID],
            "mimeType": "application/pdf",
        }
        media = MediaFileUpload(pdf_path, mimetype="application/pdf")
        
        uploaded_file = drive_service.files().create(
            body=file_metadata, media_body=media, fields="id", supportsAllDrives=True
        ).execute()
        
        print(f"✅ PDF uploaded to Google Drive: {uploaded_file['id']}")
        return uploaded_file['id']

    except Exception as e:
        print(f"❌ ERROR: Failed to upload PDF to Google Drive: {e}")
        return None

def send_to_printer(pdf_path):
    """Sends the PDF to the default printer and verifies print completion."""
    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: PDF file {pdf_path} does not exist. Cannot print.")
        return False

    try:
        print(f"🖨️ Sending {pdf_path} to printer...")
        subprocess.run(["lp", pdf_path], check=True)
        print(f"✅ Print job sent successfully: {pdf_path}")

        # ✅ Step 5: Verify print completion
        return monitor_print_queue(pdf_path)

    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to print {pdf_path}: {e}")
        return False

def monitor_print_queue(pdf_path):
    """Monitors the printer queue to confirm job completion."""
    retries = 0
    filename = os.path.basename(pdf_path)

    while retries < 5:  # Retry up to 5 times
        try:
            output = subprocess.check_output(["lpstat", "-o"], universal_newlines=True)
            if filename not in output:
                print(f"✅ Print job for {pdf_path} completed successfully!")
                return True

            print(f"⏳ Print job still in queue... Retrying in 15 seconds.")
            time.sleep(15)

        except subprocess.CalledProcessError as e:
            print(f"❌ ERROR: Failed to check print queue: {e}")

        retries += 1

    print(f"🚨 ERROR: Print job for {pdf_path} failed after multiple attempts.")
    return False
