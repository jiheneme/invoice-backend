import re
from spacy.matcher import Matcher
from app.facture.nlp_loader import nlp

def extract_invoice_number(doc):
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{"LOWER": "facture"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "n°"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "n°"}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "no"}, {"IS_SPACE": True, "OP": "?"}, {"IS_PUNCT": True}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "numéro"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": "numéro"}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"IS_PUNCT": True}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"IS_PUNCT": True}, {"IS_SPACE": True, "OP": "?"}, {"IS_DIGIT": True}],
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["no", "n°", "numéro"]}}, {"IS_PUNCT": True, "OP": "?"}, {"TEXT": {"REGEX": r"\d{4}[-–]\d+"}}],
        [{"LOWER": "facture"}, {"LOWER": {"IN": ["no", "n°", "numéro"]}}, {"TEXT": {"REGEX": r"\d+"}}],
        [{"LOWER": "facture"}, {"IS_PUNCT": True}, {"TEXT": {"REGEX": r"\d{4}[-–]?\d+"}}]
    ]
    matcher.add("INVOICE_NUMBER", patterns)

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        for token in span:
            if re.match(r"\d{4}[-–]?\d+|\d+", token.text):
                return token.text
    return None
