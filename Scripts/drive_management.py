# --- drive_management.py ---
# 🚀 Handles Google Drive operations for Work Order processing.

import os
import time
import datetime
import requests
from print_manager import send_to_printer
from googleapiclient.discovery import build
from authenticate_google import authenticate
from work_order_helpers import GID_TO_CELL_MAP
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Retrieve Google Drive & Sheets Configuration from .env
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
PARENT_FOLDER_ID = os.getenv("PARENT_FOLDER_ID")

def get_destination_folder(drive_service):
    """Gets or creates the current Year/Month folder in Google Drive."""
    current_date = datetime.datetime.now()
    year_folder_name = str(current_date.year)
    month_folder_name = current_date.strftime("%B")

    year_folder_id = find_or_create_folder(year_folder_name, PARENT_FOLDER_ID, drive_service)
    month_folder_id = find_or_create_folder(month_folder_name, year_folder_id, drive_service)

    return month_folder_id

def find_or_create_folder(folder_name, parent_folder_id, drive_service):
    """Finds or creates a folder in Google Drive."""
    query = f"name='{folder_name}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    
    try:
        results = drive_service.files().list(
            q=query, fields="files(id, name)", supportsAllDrives=True, includeItemsFromAllDrives=True
        ).execute()
        files = results.get("files", [])

        if files:
            print(f"✅ Existing folder found: {folder_name} (ID: {files[0]['id']})")
            return files[0]["id"]

        folder_metadata = {
            "name": folder_name,
            "parents": [parent_folder_id],
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = drive_service.files().create(body=folder_metadata, fields="id", supportsAllDrives=True).execute()
        print(f"✅ Created new folder: {folder_name} (ID: {folder['id']})")
        return folder["id"]

    except Exception as e:
        print(f"❌ ERROR: Google Drive API failure: {e}")
        return None

def duplicate_work_order_template(destination_folder_id, drive_service, sheets_service, task_data):
    """Updates Work Order Number in Template, then duplicates the Work Order Template."""
    
    if not TEMPLATE_ID:
        print("❌ ERROR: `TEMPLATE_ID` is missing! Cannot duplicate Work Order.")
        return None
    
    try:
        # ✅ Step 1: Increment the Work Order Number BEFORE copying
        new_work_order_number = increment_work_order_number(sheets_service, TEMPLATE_ID)
        if not new_work_order_number:
            print("❌ ERROR: Failed to increment Work Order Number.")
            return None

        # ✅ Step 2: Duplicate the Work Order Template
        file_metadata = {"name": f"Work Order {new_work_order_number}", "parents": [destination_folder_id]}
        copied_file = drive_service.files().copy(fileId=TEMPLATE_ID, body=file_metadata, supportsAllDrives=True).execute()
        new_file_id = copied_file.get("id")
        print(f"✅ Work Order Template duplicated successfully (New ID: {new_file_id})")
        
        time.sleep(2)  # 🔹 Allow time for the new file to be created

        # ✅ Step 3: Update the Work Order with Asana task data
        update_work_order_data(sheets_service, new_file_id, task_data)

        # ✅ Step 4: Export Work Order as a PDF
        pdf_path = export_work_order_to_pdf(new_file_id, drive_service)
        if not pdf_path:
            print("❌ ERROR: Failed to export Work Order to PDF.")
            return None

        # ✅ Step 5: Send to Printer
        send_to_printer(pdf_path)

        return new_file_id

    except Exception as e:
        print(f"❌ ERROR: Failed to duplicate Work Order: {e}")
        return None

def update_work_order_data(sheets_service, spreadsheet_id, task_data):
    """Updates the copied Work Order with Asana task data, correctly formatting QDMPT."""
    try:
        sheet = sheets_service.spreadsheets()
        updates = []

        if not task_data:
            print(f"❌ ERROR: No task data provided for Work Order {spreadsheet_id}.")
            return

        print(f"🔍 Preparing updates for Work Order {spreadsheet_id}...")

        for gid, cell in GID_TO_CELL_MAP.items():
            if gid in task_data and task_data[gid]:  # Ensure field has data
                if gid == "1207729443286582":  # QDMPT Field (Quantity | Description | Measurement | Price | Total)
                    qdmpt_data = task_data[gid].split("\n")  # Split by new line (each row)
                    qdmpt_values = []

                    for row in qdmpt_data:
                        columns = [col.strip() for col in row.split("|")]  # Split into columns
                        if len(columns) < 5:  # Ensure at least 5 columns
                            columns += [""] * (5 - len(columns))  # Fill missing columns with empty values
                        qdmpt_values.append(columns)

                    updates.append({"range": cell, "values": qdmpt_values})

                else:
                    updates.append({"range": cell, "values": [[task_data[gid]]]})

        # ✅ Apply updates to Google Sheets
        request_body = {"data": updates, "valueInputOption": "USER_ENTERED"}
        sheet.values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()
        print(f"✅ Successfully updated Work Order {spreadsheet_id}")

    except Exception as e:
        print(f"❌ ERROR: Failed to update Work Order {spreadsheet_id}: {e}")

def increment_work_order_number(sheets_service, spreadsheet_id):
    """Increments the Work Order Number in the Google Sheet to ensure the next order has a unique number."""
    try:
        sheet = sheets_service.spreadsheets()
        range_name = "E8"
        response = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        
        if "values" in response:
            current_number = int(response["values"][0][0])
            new_number = current_number + 1

            update_data = {"range": range_name, "values": [[str(new_number)]]}
            body = {"data": [update_data], "valueInputOption": "USER_ENTERED"}
            sheet.values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
            
            print(f"✅ Updated Work Order Number: {current_number} → {new_number}")
            return new_number  # ✅ Return the new Work Order Number

    except Exception as e:
        print(f"❌ ERROR: Failed to update Work Order Number: {e}")
        return None

def export_work_order_to_pdf(spreadsheet_id, drive_service):
    """Exports a Google Sheets work order to a PDF format and saves it locally."""
    
    pdf_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=pdf"
    headers = {"Authorization": f"Bearer {os.getenv('GOOGLE_API_TOKEN')}"}

    try:
        response = requests.get(pdf_url, headers=headers)
        if response.status_code == 200:
            pdf_path = f"/tmp/Work_Order_{spreadsheet_id}.pdf"

            with open(pdf_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Work Order exported as PDF: {pdf_path}")
            return pdf_path
        
        else:
            print(f"❌ ERROR: Failed to export Work Order {spreadsheet_id} to PDF: {response.text}")
            return None

    except Exception as e:
        print(f"❌ ERROR: Failed to export Work Order {spreadsheet_id} to PDF: {e}")
        return None
