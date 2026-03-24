# --- main_workflow.py ---
# 🚀 Main execution script for Work Order Automation

import time
from task_processor import process_asana_tasks
from drive_management import get_destination_folder, duplicate_work_order_template
from authenticate_google import authenticate

def main_loop():
    """Main loop to check Asana, process tasks, and generate work orders."""
    print("✅ Starting Work Order Automation System... Monitoring QUOTED JOBS every 30 seconds.")

    drive_service, sheets_service = authenticate()  # 🔹 Ensure authentication before loop

    while True:
        try:
            # ✅ Step 1: Check Asana for new/re-entered tasks
            new_tasks = process_asana_tasks()
            if not new_tasks:
                print("✅ No new/re-entered tasks found. System continues monitoring...")
                time.sleep(30)
                continue

            # ✅ Step 2: Process each task
            for task in new_tasks:
                process_work_order(task, drive_service, sheets_service)

        except KeyboardInterrupt:
            print("\n🛑 System stopped by user.")
            break

def process_work_order(task, drive_service, sheets_service):
    """Handles work order creation and storage."""
    destination_folder_id = get_destination_folder(drive_service)

    # ✅ Duplicate the Work Order Template
    new_work_order_id = duplicate_work_order_template(destination_folder_id, drive_service, sheets_service, task)
    if new_work_order_id:
        print(f"✅ Work Order Created Successfully: {new_work_order_id}")

if __name__ == "__main__":
    main_loop()
