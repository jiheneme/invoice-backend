from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.invoice.agent_client import query_invoice_agent #to use the AI agent
from app.invoice.mcp_server_client import query_invoice_mcp_server # to use MCP server

from app.invoice.extraction import extract_entities # To use the local NLP extraction
from app.settings import get_settings

import re
import fitz  # pymupdf

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)

origins = []

if settings.env == "dev":
    origins = ["http://localhost:3000"]
elif settings.env == "rec":
    origins = ["https://rec.monapp.com"]
elif settings.env == "prod":
    origins = ["https://monapp.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "debug": settings.debug,
        "database_url": settings.database_url,
        "env": settings.env,
    }

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code = 400, detail = "The file must be a PDF.")
    
    pdf_bytes = await file.read()
    
    try:
        doc = fitz.open(stream = pdf_bytes, filetype = "pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

       
       # print(full_text)
        
       # -1 NLP extraction
       # structured_json = extract_entities(full_text)

       # 2- Call the AI Agent
       # structured_json = await query_invoice_agent(full_text)
       # return structured_json 
    
       # 3- Call the MCP server
        structured_json = await query_invoice_mcp_server(full_text)
        return structured_json
    

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")
