import os
import pandas as pd
import hashlib
from datetime import datetime


def save_df(df, folder_path, suffix='',
            extension='pkl', journal_column='journal', journal_name=None):
    """Save a DataFrame to a file."""
    if journal_name:
        journal_name = journal_name
    else:
        journal_name = df[journal_column][0].lower().replace(' ', '-')

    today_date = datetime.today().strftime('%m-%d-%y_%H-%M-%S')
    if suffix:
        filename = f"{journal_name}_{today_date}_{suffix}.{extension}"
    else:
        filename = f"{journal_name}_{today_date}.{extension}"

    full_path = os.path.join(folder_path, filename)

    method_map = {
        'csv': ('to_csv', 'index=False'),
        'pkl': ('to_pickle', None),
    }
    method_name, kwargs = method_map[extension]
    getattr(df, method_name)(full_path, kwargs)
    return full_path


def is_pdf(filepath):
    """Check if a file is a PDF by reading the first 5 bytes."""
    with open(filepath, 'rb') as f:
        header = f.read(5)
    return header == b"%PDF-"


def incorporate_pdf_into_database(pdf_path, database_dir, df, row_indx, column_name='pdf_filename'):
    """
    Rename the PDF using MD5 hash, save it to the database directory, and
    update the corresponding row in DataFrame.
    """
    with open(pdf_path, 'rb') as f:
        file_content = f.read()
        md5_hash = hashlib.md5(file_content).hexdigest()

    new_name = f"{md5_hash}.pdf"
    os.rename(pdf_path, os.path.join(database_dir, new_name))

    df.at[row_indx, column_name] = new_name
    return df.loc[row_indx]


def mv_list_of_files_to_dir(file_list, dest_dir):
    "Move a list of files to a particular directory."
    for f in file_list:
        os.rename(f, os.path.join(dest_dir, os.path.basename(f)))


def del_rows_and_corresponding_pdfs(idx, df, pdf_folder, pdf_column='pdf_filename'):
    """Delete rows from a DataFrame and the corresponding PDF files."""
    pdf_filenames = df.loc[idx, pdf_column]
    pdf_paths = [os.path.join(pdf_folder, f) for f in pdf_filenames]
    df.drop(idx, inplace=True)
    for path in pdf_paths:
        if os.path.isfile(path):
            os.remove(path)
        else:
            print(f"File {path} does not exist. Skipping deletion.")


def calculate_date_range(df, column_name='publicationDate'):
    """
    Calculate the date range of a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to calculate the date range of.
    - column_name (str, optional): The name of the column containing the
      dates. Defaults to 'publicationDate'.

    Returns:
    - tuple: A tuple containing the start and end dates of the DataFrame.
    """
    DATE_FORMAT = '%Y-%m-%d'
    series = pd.to_datetime(df[column_name])
    min_date = series.min()
    max_date = series.max()
    return [d.strftime(DATE_FORMAT) for d in (min_date, max_date)]
