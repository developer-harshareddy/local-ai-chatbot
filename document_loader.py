
from pypdf import PdfReader
from io import BytesIO

def extract_pdf_text(uploaded_file):
    reader = PdfReader(BytesIO(uploaded_file.getvalue()))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })
    return pages