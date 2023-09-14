import os
import pandas as pd
import hashlib
from datetime import datetime


def save_df(df, folder_path, suffix='', extension='pkl'):
    """Save a DataFrame to a file."""
    today_date = datetime.today().strftime('%m-%d-%y_%H-%M-%S')
    if suffix:
        filename = f"df_{today_date}_{suffix}.{extension}"
    else:
        filename = f"df_{today_date}.{extension}"
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



def find_unique_duplicates(df, column_name):
    """
    Find unique values that are duplicated in a specific column of a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to search.
    - column_name (str): The name of the column to check for duplicate values.

    Returns:
    - np.ndarray: An array containing the unique values from the column_name 
      that appear more than once in the DataFrame, excluding NaN values.

    Example:
    >>> df = pd.DataFrame({'A': [1, 2, 2, 3, 3, 4]})
    >>> find_unique_duplicates(df, 'A')
    array([2, 3])

    Note:
    This function will not consider NaN or None values as duplicates.
    """
    duplicates = df[df[column_name].duplicated(keep=False) & df[column_name].notna()]
    return duplicates[column_name].unique()


def set_duplicates_to_none(df, column_name):
    # Find the unique duplicates
    duplicate_values = find_unique_duplicates(df, column_name)

    # Count the number of rows that will be modified
    rows_to_modify = df[df[column_name].isin(duplicate_values)]
    num_modified = len(rows_to_modify)

    # Set the value to None for rows where the value in column_name is
    # in duplicate_values
    df.loc[df[column_name].isin(duplicate_values), column_name] = None

    return num_modified


def get_all_files_in_directory(dir_path, extension=None):
    """
    Get all files in the specified directory.

    Args:
    - dir_path (str): Path to the directory
    - extension (str, optional): The file extension to filter by.

    Returns:
    - list: A list of filenames
    """
    with os.scandir(dir_path) as entries:
        if extension:
            out = [entry.name for entry in entries if entry.is_file()
                   and entry.name.endswith(extension)]
        else:
            out = [entry.name for entry in entries if entry.is_file()]
        return out


def delete_non_pdf_files(folder_path):
    """
    Delete all files in a specified folder that are not PDF files.

    Parameters:
    - folder_path (str): The path to the folder containing the files to check.

    Returns:
    - int: The number of files deleted.
    """
    deleted_files_count = 0
    files_in_folder = os.listdir(folder_path)

    for filename in files_in_folder:
        filepath = os.path.join(folder_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(filepath):
            if not is_pdf(filepath):
                os.remove(filepath)
                deleted_files_count += 1
                print(f"Deleted: {filepath}")

    return deleted_files_count
