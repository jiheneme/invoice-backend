import re
from spacy.matcher import Matcher
from app.facture.nlp_loader import nlp

def extract_invoice_number(doc) -> str | None:

    text = doc.text.strip()

    # 1) Global regex on raw text
    regex_patterns = [
        # ➤ "facture n° : 2024-03360", "facture no:ABC-001-XY", "facture numéro : ZZ-88888"
        r"facture\s+(?:n°|no|numéro)\s*:?[\s]*([\w\d]+(?:[-–][\w\d]+)+)",
        # ➤ "facture : 2024-2024", "facture:ABC-123-XYZ"
        r"facture\s*:\s*([\w\d]+(?:[-–][\w\d]+)+)",
        # ➤ "facture : 2024", "facture:123456"
        r"facture\s*:\s*([\w\d]+)",
        # ➤ "facture n°: 2024", "facture no 2024", "facture numéro 000123"
        r"facture\s+(?:n°|no|numéro)\s*:?[\s]*([\w\d]+)"
    ]

    for pattern in regex_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1)

    # 2) Fallback with SpaCy Matcher
    matcher = Matcher(nlp.vocab)
    patterns = [
        # ➤ "facture 2024"
        [{"LOWER": "facture"}, {"IS_DIGIT": True}],

        # ➤ "facture n° 2024" / "facture no 2024" / "facture numéro 2024"
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["n°", "no", "numéro"]}}, {"IS_DIGIT": True}],

        # ➤ "facture n° : 2024-03360"
        [
            {"LOWER": "facture"},
            {"LOWER": {"IN": ["n°", "no", "numéro"]}},
            {"IS_SPACE": True, "OP": "*"},
            {"IS_PUNCT": True, "TEXT": ":"},
            {"IS_SPACE": True, "OP": "*"},
            {"TEXT": {"REGEX": r"[\w\d]+(?:[-–][\w\d]+)+"}}
        ],

        # ➤ "facture : 2024-2024"
        [
            {"LOWER": "facture"},
            {"IS_PUNCT": True, "TEXT": ":"},
            {"IS_SPACE": True, "OP": "*"},
            {"TEXT": {"REGEX": r"[\w\d]+(?:[-–][\w\d]+)+"}}
        ],

        # ➤ Generic dash-separated codes anywhere
        [{"TEXT": {"REGEX": r"[\w\d]+(?:-[\w\d]+)+"}}]
    ]
    matcher.add("INVOICE_NUMBER", patterns)

    for _, start, end in matcher(doc):
        span = doc[start:end]
        # 2a) full span must match a dashed code
        if re.fullmatch(r"[\w\d]+(?:[-–][\w\d]+)+", span.text):
            return span.text
        # 2b) otherwise scan tokens
        for token in span:
            if re.fullmatch(r"[\w\d]+(?:[-–][\w\d]+)+", token.text):
                return token.text
            if re.fullmatch(r"\d{4}[-–]?\d+|\d+", token.text):
                return token.text

    return None