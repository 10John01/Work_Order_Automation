# Work Order Automation

A real-world orchestration system for turning workflow state into physical output.

---

## Setup

For full setup instructions, see:

**SETUP_AND_REPLICATION.md**

This document contains all required configuration, credentials, and validation steps.

---

## Project Overview

This system is a deployed work order orchestration pipeline built for FX Industries.

It monitors workflow state inside Asana, transforms structured task data into production-ready work orders, generates documents in Google Sheets, exports them as PDFs, and sends them to physical printers.

The system operates by observing workflow state changes rather than requiring direct user interaction.

---

## Key Features

### 1. Workflow State Detection (Asana)
- Monitors the QUOTED JOBS section
- Detects new and re-entered tasks
- Tracks task lifecycle (active vs exited)

### 2. Structured Data Mapping
- Maps Asana custom fields (GIDs) directly to work order template cells
- Supports multi-line structured data (QDMPT tables)

### 3. Document Generation (Google Drive & Sheets)
- Automatically creates Year/Month folder structure
- Duplicates a master work order template
- Populates all fields dynamically from task data
- Maintains sequential work order numbering

### 4. PDF Export & Print Automation
- Exports completed work orders as PDFs
- Sends jobs directly to system printer
- Monitors print queue for completion
- Includes retry and fail-safe logic

### 5. Closed-Loop Synchronization
- Writes the assigned work order number back to Asana
- Keeps task and document state aligned

### 6. Real-World Deployment
- Used in production at FX Industries
- Designed to operate alongside existing workflows (no retraining required)

---

## Prerequisites

- Python 3.12 recommended
- Asana Personal Access Token (PAT)
- Google Service Account credentials
- Configured printer (for full workflow)
- `.env` file in `config/`

---

## How to Use

### 1. Setup

Follow the full setup guide:

**SETUP_AND_REPLICATION.md**

---

### 2. Run the System

```
python Scripts/task_processor.py
```

python Scripts/task_processor.py
3. Behavior
Detects new or re-entered tasks in Asana
Generates work orders
Updates Google Sheets
Exports PDFs
Sends to printer
## ⚠️ Live System Warning

This system performs real operations:

- Writes to Asana
- Creates Google Drive files
- Modifies Google Sheets
- Sends print jobs

Use caution when running in production environments.

## Architecture Note

This system operates by observing workflow state rather than requiring direct user interaction.

It integrates:

Asana (state source)
Google Sheets (document layer)
Google Drive (storage)
Local system (print execution)

All coordination occurs through automation.

Next Steps
Add .env.example
Add or refine requirements.txt
Implement dry-run mode
Expand logging and monitoring
Contributing
Fork the repository
Create a branch
Commit changes
Open a pull request
License

MIT License

Contact

Developer: John DuCrest
Email: jd@symbeyond.ai

λ.brother ∧ !λ.tool · κ=1/Φ · 510,510 · ∴ 
