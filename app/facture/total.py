import re

money_pattern = re.compile(r"(\d+[.,]?\d*)\s?(EUR|USD|CHF|MAD|CAD|GBP)?", re.IGNORECASE)

def extract_total_and_currency(doc, text):
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            match = money_pattern.search(ent.text)
            if match:
                amount = float(match.group(1).replace(",", "."))
                currency = match.group(2)
                return amount, currency

    fallback = re.search(r"total\s*[:\-]?\s*(\d+[.,]?\d*)\s*(EUR|USD|CHF|MAD|CAD|GBP)?", text, re.IGNORECASE)
    if fallback:
        amount = float(fallback.group(1).replace(",", "."))
        currency = fallback.group(2)
        return amount, currency

    return None, None
