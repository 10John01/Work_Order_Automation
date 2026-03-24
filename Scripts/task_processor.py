# --- task_processor.py ---
# 🚀 Fetches, extracts, and processes Asana tasks. Tracks active and exited tasks.

import os
import json
import requests
import time
import sys
sys.path.append("/Users/johnducrest/Desktop/Work_Order_Automation/env/lib/python3.12/site-packages")  # ✅ Forces Python to find dotenv
from dotenv import load_dotenv
from asana_api_refresh import fetch_section_tasks
from work_order_helpers import GID_TO_CELL_MAP

# ✅ Load environment variables
load_dotenv("/Users/johnducrest/Desktop/Work_Order_Automation/config/.env")

# ✅ Retrieve Asana API Token & Config
ASANA_PAT = os.getenv("ASANA_PAT")
ASANA_BASE_URL = "https://app.asana.com/api/1.0"
SECTION_GID = "1209031151357628"  # ✅ QUOTED JOBS GID
QUOTED_JOBS_FILE = "/Users/johnducrest/Desktop/Work_Order_Automation/config/quoted_jobs.json"
EXITED_JOBS_FILE = "/Users/johnducrest/Desktop/Work_Order_Automation/config/exited_jobs.json"

def load_json(file_path):
    """Loads JSON data from a file, returns an empty list if file doesn't exist."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(file_path, data):
    """Saves JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def process_asana_tasks():
    """Fetches tasks from Asana's QUOTED JOBS, tracks changes, and processes them."""
    print("✅ Checking for new/re-entered tasks in QUOTED JOBS...")

    # ✅ Fetch tasks from Asana
    tasks = fetch_section_tasks(SECTION_GID)
    if not tasks:
        print("✅ No new tasks detected.")
        return []

    # ✅ Load stored task IDs
    quoted_jobs = load_json(QUOTED_JOBS_FILE)
    exited_jobs = load_json(EXITED_JOBS_FILE)

    new_tasks = []
    active_task_ids = [task["gid"] for task in tasks]

    for task in tasks:
        task_gid = task["gid"]

        # 🔍 Check if the task is **new or re-entered**
        if task_gid not in quoted_jobs:
            print(f"🆕 NEW Task Detected: {task_gid}")
            quoted_jobs.append(task_gid)  # ✅ Add to active list

            if task_gid in exited_jobs:
                print(f"🔄 Task {task_gid} RE-ENTERED QUOTED JOBS. Marking as new.")
                exited_jobs.remove(task_gid)  # ✅ Remove from exited list

            task_details = fetch_task_details(task_gid)
            task_data = extract_task_data(task_details)
            if task_data:
                print(f"✅ Processed Task: {task_gid} - {json.dumps(task_data, indent=2)}")
                new_tasks.append(task_data)

    # ✅ Detect exited tasks
    for old_task in quoted_jobs[:]:  # Copy list to safely modify while iterating
        if old_task not in active_task_ids:
            print(f"🚫 Task {old_task} EXITED QUOTED JOBS.")
            quoted_jobs.remove(old_task)
            exited_jobs.append(old_task)  # ✅ Move to exited list

    # ✅ Save updated JSON files
    save_json(QUOTED_JOBS_FILE, quoted_jobs)
    save_json(EXITED_JOBS_FILE, exited_jobs)

    return new_tasks  # ✅ Returns only new/re-entered tasks

def fetch_task_details(task_gid):
    """Fetches task details from Asana, including custom fields."""
    url = f"{ASANA_BASE_URL}/tasks/{task_gid}?opt_fields=custom_fields,name,notes"
    headers = {"Authorization": f"Bearer {ASANA_PAT}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            print(f"❌ ERROR: Failed to fetch task {task_gid} ({response.status_code}): {response.text}")
            return {}
    except Exception as e:
        print(f"❌ ERROR: Exception while fetching task {task_gid}: {e}")
        return {}

def extract_task_data(task_details):
    """Extracts relevant task data and maps it to the GID_TO_CELL_MAP."""
    if not task_details:
        return {}

    extracted_data = {"Task Name": task_details.get("name", "")}
    custom_fields = task_details.get("custom_fields", [])

    for field in custom_fields:
        gid = field["gid"]
        value = field.get("display_value", "")
        if gid in GID_TO_CELL_MAP:
            extracted_data[gid] = value

    # ✅ Include Notes separately
    extracted_data["Notes"] = task_details.get("notes", "")

    return extracted_data
if __name__ == "__main__":
    print("✅ DEBUG: Running process_asana_tasks()...")
    tasks = process_asana_tasks()
    
    if tasks:
        print(f"✅ Successfully processed {len(tasks)} tasks.")
    else:
        print("❌ ERROR: No tasks were processed. Check Asana API or JSON tracking.")

