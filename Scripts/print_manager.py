# --- print_manager.py ---
# 🚀 Manages printing Work Orders, ensures print completion, and retries failed jobs.

import os
import time
import subprocess
from googleapiclient.http import MediaIoBaseDownload
from authenticate_google import authenticate
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Authenticate Google Drive
drive_service, _ = authenticate()

# ✅ Configurations
PRINT_RETRY_LIMIT = 5  # Increased retries for reliability
PRINT_CHECK_INTERVAL = 15  # Reduced interval for quicker checks

def is_printer_online():
    """Checks if the printer is online before sending jobs."""
    try:
        output = subprocess.check_output(["lpstat", "-p"], universal_newlines=True)
        if "idle" in output or "processing" in output:
            print("✅ Printer is online and ready.")
            return True
        else:
            print("❌ ERROR: Printer is not available.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to check printer status: {e}")
        return False

def send_to_printer(pdf_path):
    """Sends a PDF file to the default printer using lp command."""
    if not os.path.exists(pdf_path):
        print(f"❌ ERROR: PDF {pdf_path} does not exist. Skipping print.")
        return False

    try:
        print(f"🖨️ Sending {pdf_path} to printer...")
        subprocess.run(["lp", pdf_path], check=True)
        print(f"✅ Print job sent successfully: {pdf_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to print {pdf_path}: {e}")
        return False

def monitor_print_queue(pdf_path):
    """Monitors the printer queue to confirm job completion."""
    retries = 0
    filename = os.path.basename(pdf_path)  # Extract only the file name

    while retries < PRINT_RETRY_LIMIT:
        try:
            output = subprocess.check_output(["lpstat", "-o"], universal_newlines=True)
            if filename not in output:  # Check only the filename
                print(f"✅ Print job for {pdf_path} completed successfully!")
                return True
            print(f"⏳ Print job still in queue... Checking again in {PRINT_CHECK_INTERVAL} seconds.")
            time.sleep(PRINT_CHECK_INTERVAL)
        except subprocess.CalledProcessError as e:
            print(f"❌ ERROR: Failed to check print queue: {e}")
        
        retries += 1
    
    print(f"🚨 ERROR: Print job for {pdf_path} failed after {PRINT_RETRY_LIMIT} attempts.")
    return False

def download_pdf_from_drive(drive_service, file_id, destination_path):
    """Downloads a PDF from Google Drive to a local file."""
    try:
        request = drive_service.files().get_media(fileId=file_id)
        with open(destination_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        print(f"✅ PDF Downloaded from Drive: {destination_path}")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to download PDF from Drive: {e}")
        return False

def process_print_job(pdf_drive_id, drive_service):
    """Downloads the PDF from Drive, sends it to the printer, and verifies success."""
    local_pdf_path = f"/tmp/Work_Order_{pdf_drive_id}.pdf"

    # ✅ Step 1: Download PDF from Drive
    if not download_pdf_from_drive(drive_service, pdf_drive_id, local_pdf_path):
        print(f"❌ ERROR: Failed to download PDF. Skipping print.")
        return False

    # ✅ Step 2: Check Printer Status
    if not is_printer_online():
        print(f"❌ ERROR: Printer is offline. Skipping print job.")
        return False

    # ✅ Step 3: Send to Printer
    if not send_to_printer(local_pdf_path):
        print(f"❌ ERROR: Print job failed: {local_pdf_path}")
        return False

    # ✅ Step 4: Monitor Print Queue
    if monitor_print_queue(local_pdf_path):
        print(f"✅ Print completed successfully: {local_pdf_path}")

        # ✅ Step 5: Clean up local copy after successful print
        os.remove(local_pdf_path)
        print(f"🗑️ Deleted local PDF: {local_pdf_path}")

        return True
    else:
        print(f"❌ ERROR: Print job did not complete successfully.")
        return False
