# README.md

## **Project Overview**
This project automates work order management by integrating Asana and Google Drive APIs. The system streamlines task creation, updates, and organization, ensuring efficient workflows at FX Industries.

### **Key Features**
1. **Asana Integration**:
   - Fetches tasks from Asana's `QUOTED JOBS` section.
   - Updates and moves tasks between stages (`Staging` to `QUOTED JOBS`).

2. **Google Drive Integration**:
   - Locates and duplicates work order templates.
   - Automatically populates templates with task data and also pulls a new work order number and populates it in the new work order.
   - Duplicates the new work order and organizes both files into a folders based on `Client Name` and `Date`.
   - Generates and prints the new order.

3. **Security**:
   - Environment variables (`.env`) securely store API keys.
   - Sensitive files excluded from version control via `.gitignore`.

---

## **Prerequisites**
### **1. Environment Setup**
- Python 3.8+
- Virtual Environment (`venv`)

### **2. Dependencies**
Install required packages:
```bash
pip install -r requirements.txt
```

### **3. API Credentials**
#### Asana API
- Register an application at [Asana Developers](https://developers.asana.com/).
- Save `client_id`, `client_secret`, and `redirect_uri` in `.env`:
  ```
  ASANA_CLIENT_ID=<your_client_id>
  ASANA_CLIENT_SECRET=<your_client_secret>
  ASANA_REDIRECT_URI=http://localhost:8081
  ```

#### Google Drive API
- Enable the Google Drive API in the [Google Cloud Console](https://console.cloud.google.com/).
- Download `client_secret_<project_id>.json` and save in the `config/` folder.
- Add to `.env`:
  ```
  GOOGLE_APPLICATION_CREDENTIALS=config/client_secret_<project_id>.json
  ```

### **4. Secure Sensitive Files**
Add the following to `.gitignore`:
```
.env
config/asana_token.json
config/client_secret_<project_id>.json
token.json
```

---

## **File Structure**
```
project-root/
|-- config/
|   |-- asana_token.json       # Asana OAuth tokens
|   |-- client_secret_<id>.json # Google API credentials
|   |-- token.json             # Google API tokens
|-- scripts/
|   |-- asana_authenticate.py  # Handles Asana OAuth
|   |-- main_workflow.py       # Main script orchestrating workflow
|   |-- folder_management.py   # Google Drive folder management
|   |-- google_docs_api.py     # Template population logic
|-- .env                       # Environment variables
|-- requirements.txt           # Python dependencies
|-- README.md                  # Project documentation
```

---

## **How to Use**

### **1. Authenticate with APIs**
#### Asana
Run the following script to authenticate with Asana and store the token:
```bash
python scripts/asana_authenticate.py
```

#### Google Drive
Ensure `GOOGLE_APPLICATION_CREDENTIALS` is set in `.env`. The first API call will prompt you to authenticate.

### **2. Execute Workflow**
Run the main script to automate the workflow:
```bash
python scripts/main_workflow.py
```

### **3. Debugging**
- **Logs**: Check logs for errors or debugging information.
- **Common Issues**:
  - Missing dependencies: Run `pip install -r requirements.txt`.
  - API authentication errors: Reauthenticate and verify tokens.

---

## **Next Steps**
- Implement token refresh logic for both APIs.
- Enhance error handling with detailed logs and retries.
- Add unit tests for individual modules.

---

## **Contributing**
- Fork the repository.
- Create a feature branch (`git checkout -b feature-name`).
- Commit your changes (`git commit -m 'Add feature'`).
- Push to the branch (`git push origin feature-name`).
- Open a pull request.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

---

## **Contact**
- **Developer**: John DuCrest
- **Email**: john@fxindustries.net
