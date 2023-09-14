import os
import pandas as pd
import PyPDF2
from core.helper_funcs import is_pdf


def list_files_not_in_dataframe(df, folder, column_name='pdf_filename'):
    """List files in a folder that are not in the DataFrame."""
    files_in_folder = [os.path.join(folder, f) for f in os.listdir(folder)]
    pdfs_in_df = [os.path.join(folder, f) for f in df[column_name] if pd.notna(f)]
    files_not_in_df = [f for f in files_in_folder if f not in pdfs_in_df]
    return files_not_in_df


def list_nonpdf_files_in_folder(folder):
    """List all non-PDF files in a folder."""
    files_in_folder = [os.path.join(folder, f) for f in os.listdir(folder)]
    nonpdf_files = [f for f in files_in_folder if not is_pdf(f)]
    return nonpdf_files


def is_pdf_corrupted(filepath, verbose=False):
    """Check whether a PDF file is corrupted."""
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


# def remove_nonpdf_files_from_dir_and_df(pdf_path, df,
#                                         column_name='pdf_filename'):
#     """
#     Remove all non-PDF files from a directory and update the
#     corresponding DataFrame.

#     This function iterates over each row in the given DataFrame,
#     checks whether the file referenced in the specified column is a
#     PDF, and removes it from both the directory and DataFrame if it is
#     not.

#     Parameters:
#     - pdf_directory (str): The directory where the PDF files are
#       located.
#     - df (DataFrame): The DataFrame containing filenames to check.
#     - column_name (str, optional): The name of the DataFrame column
#       containing filenames. Defaults to 'pdf_filename'.

#     Returns:
#     - DataFrame: The updated DataFrame with non-PDF filenames set to None.
#     """
#     for index, row in df.iterrows():
#         filename = row[column_name]

#         if pd.isna(filename):
#             continue

#         filepath = os.path.join(pdf_path, filename)

#         if not is_pdf(filepath):
#             os.remove(filepath)
#             print(f"Removed non-PDF file: {filepath}")
#             df.at[index, column_name] = None
#     return df
