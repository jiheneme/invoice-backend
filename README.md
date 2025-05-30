# 🧾 Invoice Backend
Invoice Backend is a modern backend service to extract structured data from invoice PDFs using OCR and NLP.

Built with FastAPI, Poetry, and PyMuPDF, it supports multiple modes of entity extraction:

Local NLP via spaCy

Remote inference via an AI Agent

Remote inference via an MCP Server

# 🚀 Features
📄 Upload and process invoice PDFs via API

🔍 Text extraction using PyMuPDF (fitz)

🧠 Named Entity Recognition with spaCy

🤖 Integration with Hugging Face AI Agent

🔗 Compatible with Model Context Protocol (MCP)

📦 Poetry-based dependency management

⚙️ Modular architecture for scalable document automation


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

# 🛠 Configuration
All runtime configuration is handled via the -settings.py- module. It loads environment-specific variables:

- App name

- Debug mode

- Environment (dev, rec, prod)

- CORS origins

- (Optional) External service URLs

- Set your environment using .env.dev, .env.prod, etc.

## API
POST /upload-pdf/ – Upload a PDF invoice and get structured JSON response.

🧠 Entity Extraction Modes
Inside upload_pdf() in main.py, choose one of the following methods:

1. 🔍 Local spaCy NLP :
   
   structured_json = extract_entities(full_text)
3. 🤖 AI Agent : Calls a remote Hugging Face model exposed via an AI agent microservice.

   structured_json = await query_invoice_agent(full_text)
5. 🌐 MCP Server : Uses the Model Context Protocol to invoke a compliant inference server.
   
   structured_json = await query_invoice_mcp_server(full_text)
   
#### To switch between modes, comment/uncomment the corresponding lines in main.py.

# 📄 License

This project is licensed under the MIT License – see the [LICENSE](./LICENSE) file for details.
