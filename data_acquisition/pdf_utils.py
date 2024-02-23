"""Utilities for working with PDF files."""

import os
from pypdf import PdfReader
import pdfplumber
import fitz


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


def extract_text_with_pypdf(filepath):
    """Extract text from a PDF file using pypdf."""
    with open(filepath, 'rb') as f:
        text = ""
        reader = PdfReader(f)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text += page.extract_text()
    return text


def extract_text_with_pdfplumber(filepath):
    """
    Extract text from a PDF file using pdfplumber.

    Note threshold for x and y tolerance has been lowered to improve
    segmentation.
    """
    with pdfplumber.open(filepath) as pdf:
        text = "\n".join([page.extract_text(x_tolerance=1,
                                            y_tolerance=1)
                          for page in pdf.pages])
    return text.strip()


def extract_text_with_pymupdf(filepath):
    """Extract text from a PDF using PyMuPDF."""
    with fitz.open(filepath) as doc:
        text = "\n".join([page.get_text() for page in doc])
    return text.strip()


def pdf_to_text(filepath, engine='pdfplumber'):
    """Extract text from a PDF file."""
    try:
        if not is_pdf(filepath):
            with open('not_pdf.txt', 'a') as error_file:
                error_file.write(f"{filepath}\n")
            return None

        dic_engines = {
            'pdfplumber': extract_text_with_pdfplumber,
            'pypdf': extract_text_with_pypdf,
            'pymupdf': extract_text_with_pymupdf
        }

        return dic_engines[engine](filepath)

    except Exception as e:
        with open('error_files.txt', 'a') as error_file:
            error_file.write(f"{filepath} - {str(e)}\n")
        return None
