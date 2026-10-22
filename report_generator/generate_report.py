#!/usr/bin/env python3
"""
EWB Cloud Labs - AWS VPC Peering Report PDF Generator
Renders publication-ready PDF submission report according to the Page 13 grading rubric.
"""

import os
import sys
import json
import subprocess
from datetime import datetime

DEFAULT_DATA = {
    "STUDENT_NAME": "Aditya",
    "STUDENT_BATCH": "Batch 2026-A",
    "AWS_REGION": "ap-south-1 (Mumbai)",
    "COMPLETION_DATE": datetime.now().strftime("%d %B %Y"),
    "ADMIN_IP": "49.37.12.84/32",
    "VPC_A_ID": "vpc-0a1b2c3d4e5f6001a",
    "VPC_B_ID": "vpc-0b2c3d4e5f6001b2c",
    "SUBNET_PUB_A_ID": "subnet-01pub101010a",
    "SUBNET_PRIV_A_ID": "subnet-02priv101020a",
    "SUBNET_PRIV_B_ID": "subnet-03priv102010b",
    "IGW_A_ID": "igw-0987654321fedcba0",
    "PEERING_ID": "pcx-0123456789abcdef0",
    "BASTION_INSTANCE_ID": "i-0123456789bastion",
    "BASTION_PUBLIC_IP": "13.233.45.120",
    "APP_A_INSTANCE_ID": "i-0abcdef123456appa",
    "APP_B_INSTANCE_ID": "i-0fedcba987654appb"
}

def find_edge_binary():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    template_path = os.path.join(script_dir, "report_template.html")
    config_path = os.path.join(script_dir, "student_data.json")

    # Load custom student data if present
    data = DEFAULT_DATA.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                data.update(user_data)
            print(f"[+] Loaded custom config from {config_path}")
        except Exception as e:
            print(f"[!] Warning reading config: {e}")

    # Read template
    if not os.path.exists(template_path):
        print(f"[x] Template not found at {template_path}")
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Substitute variables
    for key, val in data.items():
        placeholder = f"{{{{{key}}}}}"
        html_content = html_content.replace(placeholder, str(val))

    compiled_html_path = os.path.join(script_dir, "compiled_report.html")
    with open(compiled_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Compiled HTML saved to: {compiled_html_path}")

    # Output PDF Name
    safe_name = "".join(c for c in data["STUDENT_NAME"] if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')
    pdf_filename = f"{safe_name}_EWB_VPC_Peering.pdf"
    output_pdf_path = os.path.join(project_root, pdf_filename)

    browser_bin = find_edge_binary()
    if not browser_bin:
        print("[!] Headless browser not found. HTML report is ready to be opened in any browser and saved as PDF.")
        print(f"[+] You can open: {compiled_html_path} and press Ctrl+P -> Save as PDF.")
        return

    print(f"[+] Generating PDF with headless browser: {browser_bin}")
    cmd = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={output_pdf_path}",
        "--no-pdf-header-footer",
        compiled_html_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
            size_kb = os.path.getsize(output_pdf_path) / 1024
            print(f"[SUCCESS] PDF generated successfully: {output_pdf_path} ({size_kb:.1f} KB)")
        else:
            print("[!] PDF generation finished but output file is missing or empty.")
    except Exception as e:
        print(f"[!] Error running browser PDF export: {e}")

if __name__ == "__main__":
    main()
