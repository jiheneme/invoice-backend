import re
from app.facture.nlp_loader import nlp
from app.facture.invoice_number import extract_invoice_number
from app.facture.supplier import extract_supplier
from app.facture.person import extract_person
from app.facture.date import extract_date
from app.facture.total import extract_total_and_currency 
from app.facture.products import extract_products

def extract_entities(text: str) -> dict:
    text = text.replace("€", "EUR")
    text = re.sub(r"\s+", " ", text)

    print("✅ NLP model loaded:", nlp)

    doc = nlp(text)

    invoice_number = extract_invoice_number(doc)
    supplier = extract_supplier(doc)
    person = extract_person(doc)
    date = extract_date(doc, text)
    total, currency = extract_total_and_currency(doc, text)
    products = extract_products(text, currency)

    return {
        "supplier": supplier,
        "date": date,
        "total": total,
        "currency": currency,
        "invoice_number": invoice_number,
        "person": person,
        "products": products
    }
