# app/facture/supplier.py

import re
from spacy.tokens import Doc

def extract_supplier(text: str, doc: Doc) -> str | None:
    """
    1) Try to find a line in the invoice text that looks like a company header:
       - Entirely uppercase (possibly with numbers, &, -)
       - At least two words (e.g. 'HOTEL Ritz')
    2) Fallback: merge consecutive SpaCy ORG entities and pick the longest.
    """

    # Scan line by line for an ALL-CAPS header with 2+ words
    for line in text.splitlines():
        stripped = line.strip()
        # Only letters, numbers, spaces, &, -; at least one space → 2+ words
        if (
            re.fullmatch(r"[A-Z0-9& \-ÀÉÈÇÎÙÔÏ]+", stripped)
            and " " in stripped
        ):
            # Title-case it for readability
            return stripped.title()

    # Fallback: merge consecutive ORG ents from SpaCy
    org_ents = [ent for ent in doc.ents if ent.label_ == "ORG"]
    if org_ents:
        # Sort entities by start index
        org_ents.sort(key=lambda e: (e.start, -e.end))
        merged = []
        current = org_ents[0]
        for ent in org_ents[1:]:
            # if the next entity is immediately after or overlapping, merge
            if ent.start <= current.end:
                current = current.union(ent)  # requires spaCy ≥3.4
            else:
                merged.append(current)
                current = ent
        merged.append(current)

        # Pick the longest span (most characters)
        best = max(merged, key=lambda e: len(e.text))
        return best.text.strip().title()

    return None
