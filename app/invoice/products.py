import re

product_pattern = re.compile(r"(.{3,})\s{2,}(\d{1,3})\s{2,}(\d+[.,]?\d*)\s?(EUR|USD|CHF)?", re.IGNORECASE)

print("➡️ products.py loaded")
def extract_products(text, default_currency=None):
    product_lines = []
    lines = text.split("\n")

    for line in lines:
        match = product_pattern.search(line)
        if match:
            label = match.group(1).strip()
            quantity = int(match.group(2))
            price = float(match.group(3).replace(",", "."))
            currency = match.group(4) or default_currency
            product_lines.append({
                "label": label,
                "quantity": quantity,
                "unit_price": price,
                "currency": currency
            })
    return product_lines
