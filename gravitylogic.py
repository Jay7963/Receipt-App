# gravitylogic.py

import os
import csv
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from android.storage import primary_external_storage_path

# Logging
logging.basicConfig(
    level=logging.INFO,
    filename="receipt_system.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Global files
storage_dir = os.path.join(primary_external_storage_path(), "Download")
receipt_number_file = os.path.join(storage_dir, "receipt_number.txt")
receipt_history_file = os.path.join(storage_dir, "receipt_history.csv")

# PDF styling
customization = {
    "header_text": "GRAVITY VIT FRESH RECEIPT",
    "address": "P.O. BOX 1732-00900 KIAMBU",
    "phone": "TEL: 0721935039",
    "email": "Email: jammoh2010@gmail.com",
    "footer_text": "*Goods once sold are not Returnable*"
}

def ensure_storage_dir():
    os.makedirs(storage_dir, exist_ok=True)

def read_csv_file(filepath):
    try:
        ensure_storage_dir()
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", newline='') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        logging.exception(f"Failed to read {filepath}")
        return []

def write_csv_file(filepath, data, headers):
    try:
        ensure_storage_dir()
        with open(filepath, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        logging.exception(f"Failed to write {filepath}")

def load_items():
    try:
        items_path = os.path.join(storage_dir, "items.csv")
        if not os.path.exists(items_path):
            return {}
        with open(items_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            return {row[0]: float(row[1]) for row in reader if len(row) >= 2}
    except Exception as e:
        logging.exception("load_items failed")
        return {}

def get_next_receipt_number():
    try:
        ensure_storage_dir()
        if not os.path.exists(receipt_number_file):
            with open(receipt_number_file, 'w') as f:
                f.write("1")
                return 1
        with open(receipt_number_file, 'r+') as f:
            try:
                current = int(f.read().strip())
            except:
                current = 0
            current += 1
            f.seek(0)
            f.truncate()
            f.write(str(current))
            return current
    except Exception as e:
        logging.exception("get_next_receipt_number")
        return 0

def save_receipt_to_history(receipt_number, selected_items, grand_total, company):
    try:
        data = read_csv_file(receipt_history_file)
        data.append({
            "Receipt Number": receipt_number,
            "Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Company": company,
            "Grand Total": grand_total
        })
        write_csv_file(receipt_history_file, data, ["Receipt Number", "Date", "Company", "Grand Total"])
    except Exception as e:
        logging.exception("save_receipt_to_history")

def generate_receipt_pdf(selected_items, company):
    if company == "Select Company" or not selected_items:
        return None
    try:
        receipt_number = get_next_receipt_number()
        filename = f"receipt_{receipt_number}.pdf"
        filepath = os.path.join(storage_dir, filename)

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, y, customization["header_text"])
        y -= 20

        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, y, customization["address"])
        y -= 15
        c.drawCentredString(width/2, y, customization["phone"])
        y -= 15
        c.drawCentredString(width/2, y, customization["email"])
        y -= 25

        c.drawString(50, y, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 15
        c.drawString(50, y, f"Company: {company}")
        y -= 25

        # Header row
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Qty")
        c.drawString(100, y, "Item")
        c.drawString(250, y, "Price")
        c.drawString(350, y, "Total")
        y -= 15

        c.setFont("Helvetica", 10)
        grand_total = 0
        for item, qty, price, total in selected_items:
            c.drawString(50, y, str(qty))
            c.drawString(100, y, item)
            c.drawString(250, y, f"{price:.2f}")
            c.drawString(350, y, f"{total:.2f}")
            y -= 15
            grand_total += total

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width - 50, y, f"Grand Total: KSH {grand_total:.2f}")
        y -= 20
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width/2, y, customization["footer_text"])

        c.save()
        save_receipt_to_history(receipt_number, selected_items, grand_total, company)
        return filepath
    except Exception as e:
        logging.exception("generate_receipt_pdf")
        return None
