# --- work_order_helpers.py ---
# 🚀 Stores GID mappings and work order tracking utilities.

GID_TO_CELL_MAP = {
    "1209031151357628": "F10",  # QUOTED JOBS
    "1207729443286508": "E8",  # Work Order #
    "1207729443286499": "B4",  # Company Name
    "1208001344660510": "C10",  # Client PO #
    "1207769560056163": "F10",  # Invoice #
    "1207729443286501": "C11",  # Name
    "1207729443286510": "F11",  # Phone Number
    "1207729443286512": "F11",  # Email address (shares space)
    "1207729443286514": "C13",  # Color
    "1207759590419183": "C14",  # Color in Stock
    "1207759590419185": "F13",  # Powder Ordered
    "1207729443286528": "F14",  # Number of Pieces
    "1207729443286530": "C15",  # Date Received
    "1207729443286532": "F15",  # Lead Time
    "1207729443286534": "C16",  # Client Contacted
    "1207729443286536": "F16",  # Contacted By
    "1207923035995043": "B19",  # Media Blast
    "1207923035994973": "C19",  # Chemical Strip
    "1207729443286576": "C21",  # Job Description
    "1207729443286578": "F21",  # Location of Material
    "1207729443286582": "B24:F39",  # Quantity | Description | Measurements | Price | Total
    "1207826013374086": "C40",  # Notes
}

def increment_work_order_number(sheets_service, spreadsheet_id):
    """Increments the Work Order Number in the Google Sheet to ensure the next order has a unique number."""
    try:
        sheet = sheets_service.spreadsheets()
        range_name = "E8"  # Change this to the correct cell where Work Order Number is stored
        response = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        
        if "values" in response:
            current_number = int(response["values"][0][0])  # Convert to integer
            new_number = current_number + 1  # Increment by 1
            
            update_data = {
                "range": range_name,
                "values": [[str(new_number)]],
            }
            
            body = {"data": [update_data], "valueInputOption": "USER_ENTERED"}
            sheet.values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
            
            print(f"✅ Updated Work Order Number: {current_number} → {new_number}")

    except Exception as e:
        print(f"❌ ERROR: Failed to update Work Order Number: {e}")
