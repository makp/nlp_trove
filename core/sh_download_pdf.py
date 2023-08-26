import time
import os
import hashlib
import pandas as pd
from scidownl import scihub_download
from core.helper_funcs import is_pdf


def download_article_from_doi(url):
    out = './out.pdf'
    scihub_download(url, paper_type="doi", out=out)
    time.sleep(1)
    if not is_pdf(out):
        os.remove(out)
        return False
    return True


def move_and_rename_pdf(dest_folder):
    if not os.path.exists("./out.pdf"):
        return None

    # Generate MD5 hash
    with open("out.pdf", 'rb') as f:
        file_content = f.read()
        md5_hash = hashlib.md5(file_content).hexdigest()

    new_name = f"{md5_hash}.pdf"

    # Move the file to `dest_folder` with `new_name`
    os.rename("./out.pdf", os.path.join(dest_folder, new_name))

    return new_name


def replace_nan_with_filename(row, dest_folder):
    if pd.isna(row['pdf_filename']):
        success = download_article_from_doi(row['doi_url'])
        if success:
            return move_and_rename_pdf(dest_folder)
        else:
            return None
    else:
        return row['pdf_filename']
