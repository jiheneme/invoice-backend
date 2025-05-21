# app/facture/total_currency.py

import re
from spacy.tokens import Doc

# match amounts like "1 234,56 EUR" or "1234.56USD" or just "34"
_money_pattern = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(EUR|USD|CHF|MAD|CAD|GBP)?",
    re.IGNORECASE
)
# match a standalone "Devise : EUR" line
_currency_line = re.compile(
    r"\bdevise\b\s*[:\-]\s*([A-Za-z]{3})\b",
    re.IGNORECASE
)
# match a standalone "Total : 34" line
_total_line = re.compile(
    r"\btotal\b\s*[:\-]\s*(\d+(?:[.,]\d+)?)\b",
    re.IGNORECASE
)

# match a standalone "Montant : 34" line
_montant_line = re.compile(
    r"\bmontant\b\s*[:\-]\s*(\d+(?:[.,]\d+)?)\b",
    re.IGNORECASE
)

def extract_total_and_currency(doc: Doc, text: str) -> tuple[float | None, str | None]:
    """
    Return (amount, currency) by:
      1) scanning for an explicit 'Devise : XXX' line
      2) scanning SpaCy MONEY ents for the first match
      3) scanning for an explicit 'total : XXX' line
    """
    # Try an explicit 'Devise : EUR' line
    cur_match = _currency_line.search(text)
    currency = cur_match.group(1).upper() if cur_match else None

    # Try SpaCy MONEY ents
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            m = _money_pattern.search(ent.text)
            if m:
                amt = float(m.group(1).replace(",", "."))
                # if ent.text brought its own currency, override
                currency = (m.group(2).upper() if m.group(2) else currency)
                return amt, currency

    # Fallback on a 'Total : 34' line
    total_match = _total_line.search(text)
    if total_match:
        amt = float(total_match.group(1).replace(",", "."))
        return amt, currency
    
    # Fallback on a 'Montant : 34' line
    montant_match = _montant_line.search(text)
    if montant_match:
        amt = float(montant_match.group(1).replace(",", "."))
        return amt, currency

    return None, currency
