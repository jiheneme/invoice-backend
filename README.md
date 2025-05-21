# Invoice Backend

🚀 A backend service to extract structured data (e.g. supplier, invoice number, date, total, products, etc.) from invoice PDFs using OCR and NLP (via spaCy). Built with FastAPI and managed via Poetry.

## Features

- 🧾 Upload invoice PDFs via API
- 🔍 Text extraction with PyMuPDF (fitz)
- 🧠 Named Entity Recognition with spaCy
- 🔄 Modular pipeline: extract supplier, date, total, invoice number, people, and product lines
- ⚙️ Modern Python project structure (FastAPI, Poetry, Docker-ready)

## Getting Started

### Requirements

- Python 3.11
- Poetry
- fitz  # pymupdf

### Installation

git clone https://github.com/jiheneme/invoice-backend.git
cd invoice-backend
poetry install

### Run the server

source ./start.sh

### API
POST /upload – Upload a PDF invoice and get structured JSON response.

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.
