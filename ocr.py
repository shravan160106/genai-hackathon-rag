from mistralai import Mistral
import base64
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=api_key)

def extract_text_from_pdf(pdf_path):

    with open(pdf_path, "rb") as file:
        pdf_data = file.read()

    encoded_pdf = base64.b64encode(pdf_data).decode()

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{encoded_pdf}"
        }
    )

    pages = []

    for i, page in enumerate(response.pages):

        pages.append({
            "page": i + 1,
            "text": page.markdown
        })

    return pages