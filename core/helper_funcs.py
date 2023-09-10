import os
import pandas as pd
from datetime import datetime


def save_df(df, folder_path, extension='csv', suffix=''):
    """Save a DataFrame to a file."""
    today_date = datetime.today().strftime('%m-%d-%y_%H-%M-%S')
    if suffix:
        filename = f"df_{today_date}_{suffix}.{extension}"
    else:
        filename = f"df_{today_date}.{extension}"
    full_path = os.path.join(folder_path, filename)

    method_map = {
        'csv': 'to_csv',
        'pkl': 'to_pickle',
    }
    method_name = method_map[extension]
    getattr(df, method_name)(full_path, index=False)
    return full_path


def is_pdf(filepath):
    """Check if a file is a PDF by reading the first 5 bytes."""
    with open(filepath, 'rb') as f:
        header = f.read(5)
    return header == b"%PDF-"


def clean_non_pdf_files(pdf_path, df, column_name='pdf_filename'):
    for index, row in df.iterrows():
        filename = row[column_name]

        if pd.isna(filename):
            continue

        filepath = os.path.join(pdf_path, filename)

        if not is_pdf(filepath):
            os.remove(filepath)
            print(f"Removed non-PDF file: {filepath}")
            df.at[index, column_name] = None
    return df


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
