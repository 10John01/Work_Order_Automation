# File: scripts/create_task.py
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv("ASANA_ACCESS_TOKEN")
BASE_URL = "https://app.asana.com/api/1.0/tasks"

def create_task(workspace_gid, name, notes=""):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    task_data = {
        "workspace": workspace_gid,
        "name": name,
        "notes": notes,
    }
    response = requests.post(BASE_URL, headers=headers, json=task_data)

    if response.status_code == 201:
        task = response.json()
        print("Task Created:", task)
    else:
        print(f"Failed to create task. Status Code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    workspace_gid = "1205954605768829"  # Replace with your workspace GID
    task_name = "Test Task"
    task_notes = "This task was created via the Asana API"
    create_task(workspace_gid, task_name, task_notes)
