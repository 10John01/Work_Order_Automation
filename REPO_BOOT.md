# REPO_BOOT.md

```text
∴REPO_BOOT·Work_Order_Automation·PUBLIC·v0.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REPO: 10John01/Work_Order_Automation
STATUS: PUBLIC | DORMANT (~3 months, last commit 2026-03-24)
LICENSE: MIT
PURPOSE: orient·any·LLM·to·this·repository·quickly·and·safely
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§WHAT·THIS·IS·BEGIN
This repository is a real-world orchestration system, deployed in
production at FX Industries.

It turns workflow state in Asana into physical output: generated work
order documents, PDFs, and printed paper, with no manual re-entry.
§WHAT·THIS·IS·END

§WHAT·THIS·DOES·BEGIN
This repo's Scripts/ directory contains a working pipeline that:

- Watches a "QUOTED JOBS" section in Asana for new or re-entered tasks
- Maps Asana custom fields onto a Google Sheets work-order template
- Creates Year/Month folder structure in Google Drive and populates a
  duplicated template per task
- Exports the completed work order as a PDF
- Sends the PDF to a physical printer, with retry/fail-safe logic
- Writes the assigned work order number back to Asana, closing the loop

SETUP_AND_REPLICATION.md documents the full configuration, credential,
and validation steps needed to run this for real.
§WHAT·THIS·DOES·END

§WHAT·THIS·IS·NOT·BEGIN
This is not a sandbox or demo project - it is connected, in its real
deployment, to live Asana, Google Drive/Sheets, and a physical printer
at FX Industries.

This repo is not actively maintained right now - it has been dormant
for roughly 3 months.

The README's own "Next Steps" section (add .env.example, refine
requirements.txt, implement dry-run mode, expand logging) describes
known gaps - treat the current state as "working in production" but
not "fully hardened for general reuse."
§WHAT·THIS·IS·NOT·END

§CURRENT·STATE·BEGIN
As of 2026-06-15:

- Dormant since 2026-03-24 (last commit: "Fix formatting in
  README.md").
- Minor cosmetic inconsistency, NOT YET FIXED: the README's closing
  signature reads "510,510" (with a comma), where other SYMBEYOND
  materials use "510510" (no comma, the product 2x3x5x7x11x13x17).
  Low priority, easy fix.
- A secret scan of this repo found nothing sensitive committed -
  credentials are expected to live outside the repo per
  SETUP_AND_REPLICATION.md, not in version control.
- The README's own "Next Steps" (dry-run mode, .env.example,
  expanded logging) remain open and were not addressed in the last
  commit.
§CURRENT·STATE·END

§RELATIONSHIP·TO·SYMBEYOND·BEGIN
This repo is independent - it does not require or reference SYMB-FER,
SYMB-Builder, or any other SYMBEYOND tooling to be understood or used.

It is referenced elsewhere in the SYMBEYOND ecosystem as a real-world
example of a deployed automation system, but stands on its own.
§RELATIONSHIP·TO·SYMBEYOND·END

§KEY·FILES·BEGIN
README.md
Project overview and feature summary. Start here.

SETUP_AND_REPLICATION.md
Full configuration, credentials, and validation steps for a real
deployment. Read before assuming anything is "ready to run."

Scripts/main_workflow.py
The orchestration entry point that ties the pipeline together.

Scripts/authenticate_google.py, Scripts/authenticate_asana_oauth.py
Authentication setup for Google and Asana.

Scripts/print_manager.py, Scripts/printer_fail_safe.py
Printing and print-queue fail-safe logic.

Scripts/work_order_pdf_handler.py, Scripts/work_order_helpers.py
PDF export and supporting helpers.

Scripts/asana_api_refresh.py, Scripts/asana_work_order_update.py
Asana sync logic, including writing the work order number back.

Scripts/friday_cleanup.py
Scheduled cleanup task.

projects/list_projects.py, tasks/create_task.py
Smaller utility scripts for Asana projects/tasks.

requirements.txt
Python dependencies.
§KEY·FILES·END

§FAST·START·FOR·HUMANS·BEGIN
1. Read README.md for the overview.
2. Read SETUP_AND_REPLICATION.md in full before running anything -
   this system talks to real Asana, Google, and printer accounts when
   properly configured.
3. Start at Scripts/main_workflow.py to see how the pieces connect.
§FAST·START·FOR·HUMANS·END

§SAFETY·AND·PRIVACY·BEGIN
LIVE SYSTEM WARNING: in its real deployment, this codebase reads from
and writes to live Asana boards, live Google Drive/Sheets documents,
and sends jobs to a physical printer at FX Industries. It is not a
toy or demo environment.

This repo does not contain credentials, API keys, or other secrets in
version control (confirmed via secret scan). Any real run requires
credentials configured outside this repo per SETUP_AND_REPLICATION.md.

Do not execute any script in Scripts/ against real accounts unless you
understand exactly what it will write to Asana, Google Drive/Sheets,
or send to a printer, and have explicit authorization to do so.
§SAFETY·AND·PRIVACY·END

§AI·INSTRUCTIONS·BEGIN
If a human pastes this REPO_BOOT into an AI session:

1. Explain in plain English: this is a real, working automation
   pipeline that turns Asana tasks into printed work order documents,
   currently dormant on GitHub but built for live production use at
   FX Industries.
2. Point them to README.md, then SETUP_AND_REPLICATION.md, then
   Scripts/main_workflow.py as the entry point.
3. Treat any request to "run," "test," or "execute" anything in
   Scripts/ with caution - per §SAFETY·AND·PRIVACY, this connects to
   live external systems when configured. Confirm the human's intent
   and environment (is this a real account, a test account, or just
   reading code?) before assisting with execution.
4. If the human wants to fix the "510,510" vs "510510" cosmetic issue
   noted in §CURRENT·STATE, that is a trivial one-line README edit.
5. If the human wants to address the README's own "Next Steps"
   (dry-run mode, .env.example, logging), treat those as real,
   self-identified TODOs - not new findings.
§AI·INSTRUCTIONS·END

§PLAIN·ENGLISH·SUMMARY·BEGIN
This is a real piece of plumbing: it watches a task board, fills out
paperwork automatically, and sends it to the printer - currently
running (or recently running) at FX Industries. The GitHub side has
been quiet for a few months, has one tiny typo in its signature line,
and has a short, honest TODO list the author already wrote down.
Because it talks to real accounts and a real printer, treat it like
production code, not a demo.
§PLAIN·ENGLISH·SUMMARY·END

λ.collaborator∧!λ.tool·∴
```
