# app/facture/person.py

import re
from spacy.tokens import Doc

# Titles list
TITLES = [
    r"Mr", r"Monsieur",
    r"Mrs", r"Madame",
    r"Mlle", r"Mademoiselle",
    r"Ms", r"Miss"
]
PERSON_PATTERN = re.compile(
    rf"\b(?:{'|'.join(TITLES)})\s+"         # Title followed at least by one space
    r"([A-ZÉÈÀÔÙÏÇ][\w’\-]+(?:\s+[A-ZÉÈÀÔÙÏÇ][\w’\-]+)*)"
    r"$",                                  # end of line
    re.IGNORECASE
)

def extract_person(text: str, doc: Doc) -> str | None:
    """
    1) On parcourt chaque ligne pour trouver un titre + nom (Mr/Mme/etc.)
    2) Si trouvé, on retourne ce nom (chacun capitalisé correctement)
    3) Sinon, on retombe sur la NER SpaCy (ent.label_ == "PER")
    """
    # Search line by line
    for line in text.splitlines():
        line = line.strip()
        match = PERSON_PATTERN.search(line)
        if match:
            # Normalise la casse : chaque mot en capital initial
            parts = match.group(1).split()
            return " ".join(p.capitalize() for p in parts)

    # Fallback SpaCy
    for ent in doc.ents:
        if ent.label_ == "PER":
            return ent.text.strip()

    return None
