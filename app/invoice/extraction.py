import re
from app.invoice.nlp_loader import nlp
from app.invoice.invoice_number import extract_invoice_number
from app.invoice.supplier import extract_supplier
from app.invoice.person import extract_person
from app.invoice.date import extract_date
from app.invoice.total import extract_total_and_currency 
from app.invoice.products import extract_products

def extract_entities(text: str) -> dict:

    #print("The text without any treatements", text)
    text = text.replace("€", "EUR")

    doc = nlp(text)

    invoice_number = extract_invoice_number(doc)
    supplier = extract_supplier(text, doc)
    person = extract_person(text, doc)
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
