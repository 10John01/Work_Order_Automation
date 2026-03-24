#friday_cleanup.py
import os
import json
from datetime import datetime

# ✅ Paths to the files
CONFIG_DIR = os.path.expanduser("~/Desktop/Work_Order_Automation/config")
QUOTED_JOBS_FILE = os.path.join(CONFIG_DIR, "quoted_jobs.json")
EXITED_JOBS_FILE = os.path.join(CONFIG_DIR, "exited_jobs.json")

def clear_json_file(file_path):
    """Clears the JSON file content by resetting it to an empty list."""
    try:
        with open(file_path, "w") as f:
            json.dump([], f, indent=4)
        print(f"✅ Cleared {file_path}")
    except Exception as e:
        print(f"❌ ERROR: Failed to clear {file_path}: {e}")

def cleanup_files():
    """Checks if today is Friday and clears the files if it is."""
    if datetime.today().weekday() == 4:  # Friday is index 4
        print("🗑️ Running Friday Cleanup...")
        clear_json_file(QUOTED_JOBS_FILE)
        clear_json_file(EXITED_JOBS_FILE)
    else:
        print("ℹ️ Today is not Friday. No cleanup required.")

if __name__ == "__main__":
    cleanup_files()
