from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(chat_history):

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Notes Assistant Report", styles["Title"]))
    elements.append(Spacer(1,20))

    for chat in chat_history:

        elements.append(Paragraph(f"Question: {chat['question']}", styles["Heading3"]))
        elements.append(Paragraph(f"Answer: {chat['answer']}", styles["BodyText"]))
        elements.append(Spacer(1,10))

    path = "report.pdf"

    doc = SimpleDocTemplate(path)

    doc.build(elements)

    return path