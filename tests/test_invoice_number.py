
import sys, os
# to import "app/" without PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app.invoice.invoice_number import extract_invoice_number
from app.invoice.nlp_loader import nlp

@pytest.mark.parametrize("text,expected", [
    # ➤ Simple cases
    ("Facture 2024", "2024"),
    ("facture n° 2024", "2024"),
    ("facture no 2024", "2024"),
    ("facture numéro 2024", "2024"),
    ("facture : 2024", "2024"),

    # ➤ With spaces or ponctuation
    ("Facture no : 2024", "2024"),
    ("Facture n°: 2024", "2024"),
    ("Facture numéro : 2024", "2024"),

    # ➤ Complex format
    ("Facture no : 2024-03360", "2024-03360"),
    ("Facture n°: ABC-1234-ZX", "ABC-1234-ZX"),
    ("Facture numéro : ZZ-88888", "ZZ-88888"),
    ("facture: 123456-ZFG52-567", "123456-ZFG52-567"),

    # ➤ Edge cases
    ("Voici la facture numéro 000123", "000123"),
    ("facture: FF-GH-JK-999", "FF-GH-JK-999"),

    # ➤ Without matching
    ("Ceci est un texte sans numéro", None),
    ("La facture a été envoyée", None),
])

def test_extract_invoice_number(text, expected):
    doc = nlp(text)
    result = extract_invoice_number(doc)
    assert result == expected