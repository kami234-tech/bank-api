import fitz  # PyMuPDF
import re
from datetime import datetime

def extract_transactions(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    lines = text.split("\n")
    transactions = []

    for i in range(len(lines)):
        line = lines[i]
        match = re.match(r"(\d{2}-\d{2}-\d{4} \d{2}:\d{2})", line)
        if match:
            date_str = match.group(1)
            amount_line = " ".join(lines[i:i+4])  # Grab relevant info nearby
            amount_match = re.search(r"Suma (?:platita|retrasa) ([\d,.]+) RON", amount_line)

            # Description logic
            if "Retragere numerar" in amount_line or "Suma retrasa" in amount_line:
                description = "Retragere 💸"
            else:
                location_match = re.search(r"Locatie: (.+?)(?:\.|\sData_Ora:)", amount_line)
                description = location_match.group(1).strip() if location_match else "Tranzactie"

            if amount_match:
                try:
                    amount = float(amount_match.group(1).replace(",", "."))
                    date = datetime.strptime(date_str, "%d-%m-%Y %H:%M").strftime("%d-%m-%Y %H:%M")
                    transactions.append({
                        "amount": amount,
                        "date": date,
                        "description": description
                    })
                except Exception as e:
                    print("Parse error:", e)

    return transactions
