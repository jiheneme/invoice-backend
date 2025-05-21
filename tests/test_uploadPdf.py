import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    path = "tests/Facture_25037688.pdf"
    assert os.path.exists(path), "Le fichier de test est introuvable."

    with open(path, "rb") as f:
        response = client.post(
            "/upload-pdf/",
            files={"file": ("Facture_25037688.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200, response.text
    data = response.json()

    for key in ["supplier", "date", "total", "currency", "invoice_number", "person", "products"]:
        assert key in data, f"Missing field {key}"
    
    assert isinstance(data["supplier"], (str, type(None)))
    assert isinstance(data["date"], (str, type(None)))
    assert isinstance(data["total"], (float, int, type(None)))
    assert isinstance(data["currency"], (str, type(None)))
    assert isinstance(data["invoice_number"], (str, type(None)))
    assert isinstance(data["person"], (str, type(None)))
    assert isinstance(data["products"], list)
