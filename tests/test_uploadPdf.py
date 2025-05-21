import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_pdf():
    test_file_path = "tests/Facture_25037688.pdf"
    assert os.path.exists(test_file_path), "Le fichier de test est introuvable."

    with open(test_file_path, "rb") as f:
        response = client.post(
            "/upload-pdf/",
            files={"file": ("Facture_25037688.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200, response.text
    data = response.json()

  #On vérifie la présence de "text_extracted"
    assert "text_extracted" in data
    assert isinstance(data["text_extracted"], str)
    assert len(data["text_extracted"]) > 0
