import pytesseract
import re
from pdf2image import convert_from_path
from PIL import ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"


def extract_text_from_pdf(pdf_path):

    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)

    pages = []

    for i, img in enumerate(images):

        img = img.convert("L")

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(3)

        text = pytesseract.image_to_string(img)

        text = re.sub(r'[^a-zA-Z0-9.,\n ]', '', text)

        pages.append({
            "page": i + 1,
            "text": text
        })

    return pages