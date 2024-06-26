"""Utilities for working with PDF files."""

import os

from pypdf import PdfReader


def is_pdf(filepath):
    """Check if a file is a PDF by reading the first 5 bytes."""
    with open(filepath, "rb") as f:
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
        with open(filepath, "rb") as f:
            reader = PdfReader(f)

            # Check for valid number of pages
            if len(reader.pages) == 0:
                return True

            # Check page accessibility (raises exception)
            reader.pages[0].extract_text()

            return False
    except Exception as e:
        if verbose:
            print(f"File {filepath} may be corrupted. Error: {str(e)}")
        return True
