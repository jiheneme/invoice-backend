import re

def extract_date(doc, text):
    for ent in doc.ents:
        if ent.label_ == "DATE":
            return ent.text.strip()

    date_match = re.search(r"\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b", text)
    if date_match:
        return date_match.group(1)
    return None
