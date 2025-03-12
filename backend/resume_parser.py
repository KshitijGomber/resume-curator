import pdfplumber
from docx import Document
import io

def extract_text(file):
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(io.BytesIO(file.file.read()))
    elif file.filename.endswith(".docx"):
        return extract_text_from_docx(io.BytesIO(file.file.read()))
    else:
        return None

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])
