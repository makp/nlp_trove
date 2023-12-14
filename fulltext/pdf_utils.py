"""Utilities for working with PDF files."""

import os
import PyPDF2


def is_pdf(filepath):
    """Check if a file is a PDF by reading the first 5 bytes."""
    with open(filepath, 'rb') as f:
        header = f.read(5)
    return header == b"%PDF-"


def list_nonpdf_files_in_folder(folder):
    """List all non-PDF files in a folder."""
    files_in_folder = [os.path.join(folder, f) for f in os.listdir(folder)]
    nonpdf_files = [f for f in files_in_folder if not is_pdf(f)]
    return nonpdf_files


def is_pdf_corrupted(pdf_filename, pdf_folder, verbose=False):
    """Check whether a PDF file is corrupted."""
    filepath = os.path.join(pdf_folder, pdf_filename)
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)

            # Perform some operations to provoke an error
            reader.getNumPages()
            reader.getPage(0).extract_text()

            return False
    except Exception as e:
        if verbose:
            print(f"File {filepath} may be corrupted. Error: {str(e)}")
        return True


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


# def extract_text_from_pdf(filename, path_to_pdfs):
#     if pd.isna(filename):
#         return None

#     full_path = f"{path_to_pdfs}/{filename}"
#     return pdf_to_text(full_path)
