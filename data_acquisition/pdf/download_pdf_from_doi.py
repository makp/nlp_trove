"""Download a PDF version of an article using its DOI."""

import time
import os
import hashlib
from scidownl import scihub_download
from fulltext.pdf_utils import is_pdf


def sh_download_article_from_doi(doi):
    """Download an article using its DOI."""
    out = './out.pdf'
    url = f"https://doi.org/{doi}"
    scihub_download(url, paper_type="doi", out=out)
    time.sleep(1)
    if os.path.exists(out):
        if is_pdf(out):
            return True
        else:
            os.remove(out)
            return False
    else:
        return False


def sh_move_and_rename_pdf(dest_folder):
    """Move the downloaded PDF to `dest_folder` and rename it."""
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


def sh_download_and_rename_pdf(doi, dest_folder):
    """Download and move an article to `dest_folder` using its DOI."""
    success = sh_download_article_from_doi(doi)
    if success:
        return sh_move_and_rename_pdf(dest_folder)
    else:
        return None
