# Work Order Automation

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
This project automates work order management by integrating Asana and Google Drive APIs. It streamlines task creation, updates, and organization, ensuring efficient workflows at FX Industries.

## Key Features

### 1. Asana Integration
- Fetches tasks from Asana's `QUOTED JOBS` section.
- Updates and moves tasks between stages (`Staging` to `QUOTED JOBS`).

### 2. Google Drive Integration
- Locates and duplicates work order templates.
- Populates templates with task data, pulls new work order numbers, and organizes files into folders based on client name and date.
- Automatically generates and prints new work orders.

### 3. Security
- `.env` file securely stores API keys.
- Sensitive files are excluded from version control via `.gitignore`.

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
|-- scripts/
|   |-- asana_authenticate.py  # Handles Asana OAuth
|   |-- main_workflow.py       # Main script orchestrating workflow
|   |-- folder_management.py   # Google Drive folder management
|   |-- google_docs_api.py     # Template population logic
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
python scripts/asana_authenticate.py
```

#### Google Drive
Ensure `GOOGLE_APPLICATION_CREDENTIALS` is set in `.env`. The first API call will prompt you to authenticate.

### 2. Execute Workflow
Run the main script to automate the workflow:
```bash
python scripts/main_workflow.py
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
Email: john@fxindustries.net

