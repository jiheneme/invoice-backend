def extract_person(doc):
    for ent in doc.ents:
        if ent.label_ == "PER":
            return ent.text.strip()
    return None
