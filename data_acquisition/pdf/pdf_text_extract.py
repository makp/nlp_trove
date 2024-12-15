"""
Class to extract text from PDF files using different libraries.

Notes about the libraries used:
- `pdfplumber` is built on top of `pdfminer.six`.
- `pypdf` can do other things than text extraction such as cropping, merging,
  etc.
- `pdfplumber` has different options for controlling how words are identified
  (e.g., `x_tolerance` and `x_tolerance_ratio`). `pypdf` has the par
  `space_width` and a multiplier called `layout_mode_scale_weight`. AFAIK
  `PyMuPDF` doesn't have kwargs to adjust how words are identified.
"""

import pdfplumber
import pymupdf
from pypdf import PdfReader

from .pdf_utils import is_pdf


class PDFTextExtractor:
    def __init__(self):
        """Initialize the PDFTextExtractor class."""
        self.engines = {
            "pdfplumber": self.extract_text_with_pdfplumber,
            "pypdf": self.extract_text_with_pypdf,
            "pymupdf": self.extract_text_with_pymupdf,
            "tesseract": self.extract_text_with_tesseract,
        }

    def extract_text_with_pypdf(self, filepath, **kwargs):
        """Extract text from a PDF file using pypdf."""
        with open(filepath, "rb") as f:
            text = ""
            reader = PdfReader(f)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text += page.extract_text(**kwargs)
        return text

    def extract_text_with_pdfplumber(self, filepath, **kwargs):
        """Extract text from a PDF file using pdfplumber."""
        with pdfplumber.open(filepath) as pdf:
            text = "\n".join([page.extract_text(**kwargs) for page in pdf.pages])
        return text.strip()

    def extract_text_with_pymupdf(self, filepath, **kwargs):
        """Extract text from a PDF using PyMuPDF."""
        with pymupdf.open(filepath) as doc:
            text = "\n".join([page.get_text(**kwargs) for page in doc])  # type: ignore
        return text.strip()

    def extract_text_with_tesseract(self, filepath, **kwargs):
        """Extract text from a PDF using Tesseract via `PyMuPDF`."""
        with pymupdf.open(filepath) as doc:
            text = "\n".join(
                [
                    page.get_textpage_ocr(  # type: ignore
                        language="eng", tessdata="/usr/share/tessdata/", **kwargs
                    ).extractText()
                    for page in doc
                ]
            )
        return text.strip()

    def pdf_to_text(self, filepath, engine="pdfplumber", **kwargs):
        """Extract text from a PDF file."""
        try:
            if not is_pdf(filepath):
                with open("not_pdf.txt", "a") as error_file:
                    error_file.write(f"{filepath}\n")
                return None

            return self.engines[engine](filepath, **kwargs)

        except Exception as e:
            with open("error_files.txt", "a") as error_file:
                error_file.write(f"{filepath} - {str(e)}\n")
            return None
