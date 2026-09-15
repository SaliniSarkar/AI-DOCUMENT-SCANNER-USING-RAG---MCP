from loaders.pdf_loader import load_pdf
from loaders.excel_loader import load_excel
from loaders.csv_loader import load_csv
from loaders.docx_loader import load_docx
from loaders.image_loader import load_image


def load_document(uploaded_file, model_name="Gemini"):
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return load_pdf(uploaded_file)
    if filename.endswith((".xlsx", ".xls")):
        return load_excel(uploaded_file)
    if filename.endswith(".csv"):
        return load_csv(uploaded_file)
    if filename.endswith(".docx"):
        return load_docx(uploaded_file)
    if filename.endswith((".png", ".jpg", ".jpeg")):
        return load_image(uploaded_file, model_name=model_name)

    raise ValueError("Unsupported file type.")
