import os
import hashlib


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


def del_rows_and_corresponding_pdfs(idx, df, pdf_folder, pdf_column='pdf_filename'):
    """Delete rows from a DataFrame and the corresponding PDF files."""
    if isinstance(idx, int):
        idx = [idx]
    pdf_filenames = df.loc[idx, pdf_column]
    pdf_paths = [os.path.join(pdf_folder, f) for f in pdf_filenames]
    df.drop(idx, inplace=True)
    print(f"Rows {idx} deleted from DataFrame.")
    for path in pdf_paths:
        if os.path.isfile(path):
            os.remove(path)
            print(f"File {path} deleted.")
        else:
            print(f"File {path} does not exist. Skipping deletion.")
