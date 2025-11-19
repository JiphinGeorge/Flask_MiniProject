from PyPDF2 import PdfReader

def extract_text_from_pdf(path):
    try:
        reader = PdfReader(path)
        pages = []

        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                pages.append(txt)

        return "\n".join(pages)

    except Exception as e:
        print("PDF extraction error:", e)
        return ""
