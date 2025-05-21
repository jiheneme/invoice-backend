from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.facture.extraction import extract_entities
from app.settings import get_settings
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
        raise HTTPException(status_code=400, detail="The file must be a PDF.")
    
    pdf_bytes = await file.read()
    
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        # 🧠 NLP extraction
        structured_json = extract_entities(full_text)
        return structured_json
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")
