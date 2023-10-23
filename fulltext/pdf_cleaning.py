import os
import PyPDF2


def is_pdf(filepath):
    """Check if a file is a PDF by reading the first 5 bytes."""
    with open(filepath, 'rb') as f:
        header = f.read(5)
    return header == b"%PDF-"


def verify_pdf_filenames_and_pdfs_mismatch(df, folder, column_name='pdf_filename'):
    """Check whether PDF filenames in DataFrame and those in the PDF folder match."""
    pdfs_in_df = set(df[column_name])
    pdfs_in_folder = set(os.listdir(folder))
    if pdfs_in_df == pdfs_in_folder:
        return 0
    else:
        comp1 = pdfs_in_folder - pdfs_in_df
        comp2 = pdfs_in_df - pdfs_in_folder
        print(f"PDFs in folder but not in DataFrame\n {len(comp1)}")
        print(f"PDF filenames in DataFrame but not in the folder\n {len(comp2)}")
        return comp1, comp2


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
