# printer_fail_safe.py
# 🚀 This script ensures print jobs complete and handles printer errors gracefully.

import os
import time
import subprocess
from fpdf import FPDF

# ✅ Configurations
PRINT_RETRY_LIMIT = 3  # Number of retries before failing
PRINT_CHECK_INTERVAL = 25  # Seconds between printer queue checks
TEST_PDF_PATH = "/tmp/test_work_order.pdf"

def create_test_pdf(pdf_path):
    """Creates a simple test PDF to ensure a valid file exists for printing."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test Work Order", ln=True, align="C")
    pdf.output(pdf_path)
    print(f"✅ Test PDF created: {pdf_path}")

def is_printer_online():
    """Checks if the printer is online before sending jobs."""
    try:
        output = subprocess.check_output(["lpstat", "-p"], universal_newlines=True)
        if "idle" in output or "processing" in output:
            print("✅ Printer is online and ready.")
            return True
        else:
            print("❌ ERROR: Printer is not available.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to check printer status: {e}")
        return False

def send_to_printer(pdf_path):
    """Sends a PDF file to the default printer using the lp command."""
    try:
        print(f"🖨️ Sending {pdf_path} to printer...")
        subprocess.run(["lp", pdf_path], check=True)
        print(f"✅ Print job sent successfully: {pdf_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: Failed to print {pdf_path}: {e}")
        return False

def monitor_print_queue(pdf_path):
    """Monitors the printer queue to confirm job completion."""
    retries = 0
    while retries < PRINT_RETRY_LIMIT:
        try:
            output = subprocess.check_output(["lpstat", "-o"], universal_newlines=True)
            if pdf_path not in output:
                print(f"✅ Print job for {pdf_path} completed successfully!")
                return True
            print(f"⏳ Print job still in queue... Checking again in {PRINT_CHECK_INTERVAL} seconds.")
            time.sleep(PRINT_CHECK_INTERVAL)
        except subprocess.CalledProcessError as e:
            print(f"❌ ERROR: Failed to check print queue: {e}")
        
        retries += 1
    
    print(f"🚨 ERROR: Print job for {pdf_path} failed after {PRINT_RETRY_LIMIT} attempts.")
    return False

if __name__ == "__main__":
    create_test_pdf(TEST_PDF_PATH)  # ✅ Ensure test PDF exists before printing
    if is_printer_online():
        if send_to_printer(TEST_PDF_PATH):
            monitor_print_queue(TEST_PDF_PATH)
    print("🚀 Printer Fail-Safe System Complete!")
