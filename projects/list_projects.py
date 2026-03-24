# File: scripts/list_projects.py
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv("ASANA_ACCESS_TOKEN")
BASE_URL = "https://app.asana.com/api/1.0/projects"

def list_projects():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(BASE_URL, headers=headers)

    if response.status_code == 200:
        projects = response.json()
        print("Projects:", projects)
    else:
        print(f"Failed to fetch projects. Status Code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    list_projects()
