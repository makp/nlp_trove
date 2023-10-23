from bs4 import BeautifulSoup
import pandas as pd
import PyPDF2
from core.helper_funcs import is_pdf


def pdf_to_text(filepath):
    """Extract text from a PDF file."""
    try:
        if not is_pdf(filepath):
            with open('not_pdf.txt', 'a') as error_file:
                error_file.write(f"{filepath}\n")
            return None

        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            text = ""
            for i in range(reader.numPages):
                page = reader.getPage(i)
                text += page.extractText()
            return text
    except Exception as e:
        with open('error_files.txt', 'a') as error_file:
            error_file.write(f"{filepath} - {str(e)}\n")
        return None


def extract_text_from_pdf(filename, path_to_pdfs):
    """Extract text from PDF based on a given DataFrame row and path
    to PDFs."""
    if pd.isna(filename):
        return None

    full_path = f"{path_to_pdfs}/{filename}"
    return pdf_to_text(full_path)
