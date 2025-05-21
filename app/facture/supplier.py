def extract_supplier(doc):
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text.strip()
    return None
