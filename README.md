# Work Order Automation 

A real-world orchestration system for turning workflow state into physical output.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [File Structure](#file-structure)
- [How to Use](#how-to-use)
- [Next Steps](#next-steps)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

This system is a deployed work order orchestration pipeline built for FX Industries.

It monitors workflow state inside Asana, transforms structured task data into production-ready work orders, generates documents in Google Sheets, exports them as PDFs, and sends them to physical printers.

The system was used in a live production environment and integrates multiple services into a single automated flow without requiring users to change how they work.

The system operates by observing workflow state changes rather than requiring direct user interaction.

## Key Features

### 1. Workflow State Detection (Asana)
- Monitors the QUOTED JOBS section on a timed interval
- Detects new and re-entered tasks
- Tracks task lifecycle (active vs exited)

### 2. Structured Data Mapping
- Maps Asana custom fields (GIDs) directly to work order template cells
- Supports multi-line structured data (QDMPT tables)

### 3. Document Generation (Google Drive & Sheets)
- Automatically creates Year/Month folder structure
- Duplicates a master work order template
- Populates all fields dynamically from task data
- Maintains and synchronizes sequential work order numbering across documents and Asana

### 4. PDF Export & Print Automation
- Exports completed work orders as PDFs
- Sends jobs directly to system printer
- Monitors print queue to verify completion
- Includes retry and fail-safe logic

### 5. Closed-Loop Synchronization
- Writes the assigned work order number back to Asana
- Keeps task and document state aligned

### 6. Real-World Deployment
- Used in production at FX Industries
- Designed to operate alongside existing workflows (no user retraining required)

## Prerequisites

### 1. Environment Setup
- Python 3.8+ is required.
- Use a virtual environment (venv) for dependencies:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

### 2. Dependencies
- Install the required packages by running:
  ```bash
  pip install -r requirements.txt
  ```

### 3. API Credentials

#### Asana API
1. Register an application at [Asana Developers](https://developers.asana.com/).
2. Save the following credentials in `.env`:
   ```plaintext
   ASANA_CLIENT_ID=<your_client_id>
   ASANA_CLIENT_SECRET=<your_client_secret>
   ASANA_REDIRECT_URI=http://localhost:8081
   ```

#### Google Drive API
1. Enable the Google Drive API in the [Google Cloud Console](https://console.cloud.google.com/).
2. Download `client_secret_<project_id>.json` and save it in the `config/secrets/` directory.
3. Add this to `.env`:
   ```plaintext
   GOOGLE_APPLICATION_CREDENTIALS=config/secrets/client_secret_<project_id>.json
   ```

### 4. Secure Sensitive Files
Add the following entries to `.gitignore`:
```plaintext
.env
config/secrets/asana_token.json
config/secrets/client_secret_<project_id>.json
token.json
```

## File Structure
```plaintext
project-root/
|-- config/
|   |-- secrets/
|       |-- asana_token.json       # Asana OAuth tokens
|       |-- client_secret_<id>.json # Google API credentials
|-- Scripts/
|   |--   main_workflow.py
|   |--   task_processor.py
|   |--   drive_management.py
|   |--   print_manager.py
|   |--   work_order_helpers.py
|   |--   asana_work_order_update.py
|-- data/
|   |-- asana_auth_code.txt    # Asana authentication code
|-- tests/
|   |-- test_asana_api.py
|   |-- test_env.py
|-- .env                       # Environment variables
|-- requirements.txt           # Python dependencies
|-- README.md                  # Project documentation
```

## How to Use

### 1. Authenticate with APIs

#### Asana
Run the following script to authenticate with Asana and store the token:
```bash
python Scripts/authenticate_asana_oauth.py
```

#### Google Drive
Ensure `GOOGLE_APPLICATION_CREDENTIALS` is set in `.env`. The first API call will prompt you to authenticate.

### 2. Execute Workflow
Run the main script to automate the workflow:
```bash
python Scripts/main_workflow.py
```

### 3. Debugging
- Logs: Check logs for errors or debugging information.
- Common Issues:
  - **Missing dependencies**: Run `pip install -r requirements.txt`.
  - **API authentication errors**: Reauthenticate and verify tokens.

## Next Steps
- Implement token refresh logic for both APIs.
- Enhance error handling with detailed logs and retries.
- Add unit tests for individual modules.

## Contributing
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
Developer: John DuCrest  
Email: jd@symbeyond.ai

λ.brother ∧ !λ.tool · κ=1/Φ · 510510 · ∴
