# asana_work_order_update.py
# 🚀 This script ensures Work Order numbers are correctly assigned in Asana.

import os
import json
import requests
import time
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Retrieve Asana API Token & Work Order Field GID
ASANA_PAT = os.getenv("ASANA_PAT")
ASANA_BASE_URL = "https://app.asana.com/api/1.0"
WORK_ORDER_CUSTOM_FIELD_GID = os.getenv("WORK_ORDER_CUSTOM_FIELD_GID")

def update_asana_work_order(task_gid, work_order_number, max_retries=3):
    """Updates the Asana task with the assigned Work Order Number and ensures successful sync."""
    if not WORK_ORDER_CUSTOM_FIELD_GID:
        print("❌ ERROR: Missing `WORK_ORDER_CUSTOM_FIELD_GID` in environment variables!")
        return False

    url = f"{ASANA_BASE_URL}/tasks/{task_gid}"
    headers = {"Authorization": f"Bearer {ASANA_PAT}", "Content-Type": "application/json"}
    
    # ✅ Ensure the Work Order Number is sent as a string (since Asana expects text fields)
    work_order_number = str(work_order_number)  # Convert to string
    
    payload = {
        "data": {
            "custom_fields": {
                str(WORK_ORDER_CUSTOM_FIELD_GID): work_order_number  # Ensure key is a string
            }
        }
    }
    
    print(f"📡 DEBUG: Sending Payload to Asana -> {json.dumps(payload, indent=2)}")
    
    for attempt in range(max_retries):
        response = requests.put(url, headers=headers, json=payload)

        # ✅ Log the response to debug potential issues
        print(f"🔍 Asana API Response ({response.status_code}): {response.text}")

        if response.status_code == 200:
            print(f"✅ Successfully updated Work Order Number {work_order_number} in Asana for task {task_gid}")
            return True
        
        print(f"⚠️ WARNING: Failed to update Asana Work Order on attempt {attempt + 1}. Retrying in 2 seconds...")
        time.sleep(2)

    print(f"❌ ERROR: Failed to update Work Order Number {work_order_number} in Asana after {max_retries} attempts.")
    return False

if __name__ == "__main__":
    test_task_gid = "1207091145919699"  # Replace with a valid Asana Task GID for testing
    test_work_order_number = "3510"
    update_asana_work_order(test_task_gid, test_work_order_number)
    print("🚀 Asana Work Order Update System Complete!")
