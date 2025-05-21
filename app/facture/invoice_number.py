import re
from spacy.matcher import Matcher
from app.facture.nlp_loader import nlp

def extract_invoice_number(doc):
    text = doc.text.strip()

    # --------------------
    # Part 1 : Regex only
    # --------------------
    regex_patterns = [
        # ➤ Exemple : "Facture no : 2024-03360", "Facture n°: ABC-001-XY", "facture numéro : ZZ-88888"
        r"facture\s+(?:n°|no|numéro)\s*:?[\s]*([\w\d]+(?:[-–][\w\d]+)+)",

        # ➤ Exemple : "facture no : 2024", "facture numéro: 123456"
        r"facture\s+(?:n°|no|numéro)\s*:?[\s]*([\w\d]+)"
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    # --------------------
    # Part 2 : Fallback with SpaCy + Matcher
    # --------------------
    matcher = Matcher(nlp.vocab)
    patterns = [
        # ➤ "facture 2024"
        [{"LOWER": "facture"}, {"IS_DIGIT": True}],

        # ➤ "facture n° 2024"
        [{"LOWER": "facture"}, {"LOWER": "n°"}, {"IS_DIGIT": True}],

        # ➤ "facture n°  2024" (avec espace)
        [{"LOWER": "facture"}, {"LOWER": "n°"}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],

        # ➤ "facture no 2024"
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_DIGIT": True}],

        # ➤ "facture no  2024"
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],

        # ➤ "facture no - 2024"
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_SPACE": True, "OP": "?"}, {"IS_PUNCT": True}, {"IS_DIGIT": True}],

        # ➤ "facture numéro 2024"
        [{"LOWER": "facture"}, {"LOWER": "numéro"}, {"IS_DIGIT": True}],

        # ➤ "facture numéro  2024"
        [{"LOWER": "facture"}, {"LOWER": "numéro"}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],

        # ➤ "facture: 2024"
        [{"LOWER": "facture"}, {"IS_PUNCT": True}, {"IS_DIGIT": True}],

        # ➤ "facture :  2024"
        [{"LOWER": "facture"}, {"IS_PUNCT": True}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],

        # ➤ "facture no 2024-03360", "facture n°: 2023-01"
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["no", "n°", "numéro"]}}, {"IS_PUNCT": True, "OP": "?"}, {"TEXT": {"REGEX": r"\d{4}[-–]\d+"}}],

        # ➤ "facture no 122334"
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["no", "n°", "numéro"]}}, {"TEXT": {"REGEX": r"\d+"}}],

        # ➤ "facture: 2024-01"
        [{"LOWER": "facture"}, {"IS_PUNCT": True}, {"TEXT": {"REGEX": r"\d{4}[-–]?\d+"}}],

        # ➤ Numéro avec tirets uniquement
        [{"TEXT": {"REGEX": r"[\w\d]+(?:-[\w\d]+)+"}}],

        # ➤ "facture n°: 2024", "facture no : 2024", etc.
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["n°", "no", "numéro"]}}, {"IS_PUNCT": True}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],

        # ➤ "facture no : 2024-03360" alphanum avec tirets
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_PUNCT": True}, {"IS_SPACE": True, "OP": "?"}, {"TEXT": {"REGEX": r"[\w\d]+(?:[-–][\w\d]+)+"}}]
    ]

    matcher.add("INVOICE_NUMBER", patterns)

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        for token in span:
            # ➤ Extraction alphanumérique avec tirets : ex. "ABC-1234-ZX"
            if re.match(r"\b[\w\d]+(?:-[\w\d]+)+\b", token.text):
                return token.text
            # ➤ Extraction de formats numériques classiques : "2024-001", "123456"
            if re.match(r"\d{4}[-–]?\d+|\d+", token.text):
                return token.text

    return None
