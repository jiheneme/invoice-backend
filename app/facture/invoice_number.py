# app/facture/invoice_number.py

import re
from spacy.matcher import Matcher
from app.facture.nlp_loader import nlp

def extract_invoice_number(doc) -> str | None:

    # 1) Try global regex on the raw text
    text = doc.text.strip()
    regex_patterns = [
        # ➤ Formats with at least one dash segment
        r"facture\s+(?:n°|no|numéro)\s*:?[\s]*([\w\d]+(?:[-–][\w\d]+)+)",
        # ➤ Simple identifiers
        r"facture\s+(?:n°|no|numéro)\s*:?[\s]*([\w\d]+)"
    ]
    for pattern in regex_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1)

    # 2) Fallback using SpaCy Matcher
    matcher = Matcher(nlp.vocab)
    patterns = [
        # ➤ "facture 2024"
        [{"LOWER": "facture"}, {"IS_DIGIT": True}],

        # ➤ "facture n° 2024" or "facture no 2024" or "facture numéro 2024"
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["n°", "no", "numéro"]}}, {"IS_DIGIT": True}],

        # ➤ "facture n° : 2024-03360" with optional spaces
        [
            {"LOWER": "facture"},
            {"LOWER": {"IN": ["n°", "no", "numéro"]}},
            {"IS_SPACE": True, "OP": "*"},
            {"IS_PUNCT": True, "TEXT": ":"},
            {"IS_SPACE": True, "OP": "*"},
            {"TEXT": {"REGEX": r"[\w\d]+(?:[-–][\w\d]+)+"}}
        ],

        # ➤ Generic dash-separated codes: "123456-ZFG52-567", "FFGH-GGHJK-GHJ-GGHJ"
        [{"TEXT": {"REGEX": r"[\w\d]+(?:-[\w\d]+)+"}}]
    ]
    matcher.add("INVOICE_NUMBER", patterns)

    matches = matcher(doc)
    for _, start, end in matches:
        span = doc[start:end]
        # First try full span
        if re.fullmatch(r"[\w\d]+(?:[-–][\w\d]+)+", span.text):
            return span.text
        # Otherwise scan tokens
        for token in span:
            if re.fullmatch(r"[\w\d]+(?:[-–][\w\d]+)+", token.text):
                return token.text
            if re.fullmatch(r"\d{4}[-–]?\d+|\d+", token.text):
                return token.text

    return None
