# SETUP_AND_REPLICATION.md

## Purpose
This document explains how to recreate and run the system without machine-specific paths.

---

## System Overview
1. Reads tasks from Asana
2. Detects new tasks
3. Extracts data
4. Duplicates Google Sheet
5. Fills data
6. Exports PDF
7. Prints
8. Tracks state

---

## Requirements
- Python 3.12
- Asana PAT
- Google service account
- Printer
- .env file
  - Do NOT commit this file
  - It contains secrets
  - Ensure it is included in `.gitignore`

---

## Repository Structure

Work_Order_Automation/
- Scripts/
- config/
  - .env
  - quoted_jobs.json
  - exited_jobs.json
  - service_account.json
- legacy/
- README.md
- SETUP_AND_REPLICATION.md

---

## 1. Clone

git clone https://github.com/10John01/Work_Order_Automation.git
cd Work_Order_Automation

---

## 2. Environment

conda create -n work_order_automation python=3.12 -y
conda activate work_order_automation

---

## 3. Dependencies

pip install -r requirements.txt

or

pip install python-dotenv requests google-api-python-client google-auth

---

## 4. Config

mkdir -p config

---

## 5. JSON Files

quoted_jobs.json
[]

exited_jobs.json
[]

---

## 6. .env

ASANA_PAT=
ASANA_CLIENT_ID=
ASANA_CLIENT_SECRET=
WORK_ORDER_CUSTOM_FIELD_GID=

TEMPLATE_ID=
PARENT_FOLDER_ID=

GOOGLE_CREDENTIALS_PATH=config/service_account.json
GOOGLE_API_TOKEN=

RENDER=false

---

## 7. Google Setup (CRITICAL)

- Create service account
- Download JSON
- Place in config/service_account.json

IMPORTANT:
Share access with service account email on:
- Google Sheet template
- Google Drive folder

---

## 8. Validate

python Scripts/authenticate_asana_oauth.py
python Scripts/task_processor.py

---

## 9. WARNING

This system:
- writes to Asana
- creates Drive files
- prints

---

## 10. Checklist

- .env created
- JSON files created
- Google credentials added
- Shared with service account
- Dependencies installed

---

## Final

No absolute paths. Fully portable.
