# --- asana_api_refresh.py ---
# 🚀 Handles updating Asana tasks & retrieving task details.

import requests
import json
import os
import time
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Retrieve Asana API Token & Work Order Field GID
ASANA_PAT = os.getenv("ASANA_PAT")
ASANA_BASE_URL = "https://app.asana.com/api/1.0"
WORK_ORDER_CUSTOM_FIELD_GID = os.getenv("WORK_ORDER_CUSTOM_FIELD_GID")

def fetch_section_tasks(section_gid):
    """Fetches tasks from a specific section in Asana."""
    url = f"{ASANA_BASE_URL}/sections/{section_gid}/tasks"
    headers = {"Authorization": f"Bearer {ASANA_PAT}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print(f"❌ ERROR Fetching Tasks ({response.status_code}): {response.text}")
            return []
    except Exception as e:
        print(f"❌ ERROR: Failed to fetch tasks: {e}")
        return []

def fetch_task_details(task_gid):
    """Fetches full details of a specific Asana task, including custom fields."""
    url = f"{ASANA_BASE_URL}/tasks/{task_gid}?opt_fields=name,notes,custom_fields.gid,custom_fields.text_value,custom_fields.number_value,custom_fields.display_value"
    headers = {"Authorization": f"Bearer {ASANA_PAT}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            task_data = response.json().get("data", {})
            print(f"✅ Fetched Task Details for {task_gid}: {json.dumps(task_data, indent=2)}")
            return task_data
        else:
            print(f"❌ ERROR Fetching Task {task_gid} ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR: Failed to fetch task details: {e}")
        return None

def update_asana_work_order(task_gid, work_order_number, max_retries=3):
    """Updates the Asana task with the assigned Work Order Number and ensures successful sync."""
    if not WORK_ORDER_CUSTOM_FIELD_GID:
        print("❌ ERROR: Missing `WORK_ORDER_CUSTOM_FIELD_GID` in environment variables!")
        return False

    if not ASANA_PAT:
        print("❌ ERROR: ASANA_PAT is missing! Check your .env file.")
        return False

    url = f"{ASANA_BASE_URL}/tasks/{task_gid}"
    headers = {"Authorization": f"Bearer {ASANA_PAT}", "Content-Type": "application/json"}
    
    payload = {
        "data": {
            "custom_fields": {
                WORK_ORDER_CUSTOM_FIELD_GID: work_order_number
            }
        }
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.put(url, headers=headers, json=payload, timeout=10)
            print(f"🔍 Asana API Response ({response.status_code}): {response.text}")

            if response.status_code == 200:
                print(f"✅ Successfully updated Work Order Number {work_order_number} in Asana for task {task_gid}")
                return True
            else:
                print(f"⚠️ WARNING: Failed to update Asana Work Order on attempt {attempt + 1}. Retrying in 2 seconds...")
                time.sleep(2)
        except requests.exceptions.Timeout:
            print(f"⏳ ERROR: Timeout occurred while updating Asana Work Order for task {task_gid}. Retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"❌ ERROR: Failed to update Asana Work Order due to an exception: {e}")
            return False

    print(f"❌ ERROR: Failed to update Work Order Number {work_order_number} in Asana after {max_retries} attempts.")
    return False
