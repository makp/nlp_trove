import requests
import time
import os
import hashlib


def download_pdf_from_url(url, output_dir='', headers=None):
    if headers is None:
        headers = {}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        content_type = response.headers.get("content-type", '')
        if 'application/pdf' not in content_type:
            with open("redirected_urls_pdf_url.txt", "a") as f:
                f.write(url + "\n")
            return None

        if response.content[:5] != b'%PDF-':
            with open("redirected_urls_pdf_url.txt", "a") as f:
                f.write(url + "\n")
            return None

        hash_object = hashlib.md5(response.content)
        filename = os.path.join(output_dir, f"{hash_object.hexdigest()}.pdf")
        if os.path.exists(filename):
            print(f"File {filename} already exists. Skipping download.")
            return os.path.basename(filename)

        with open(filename, 'wb') as f:
            f.write(response.content)
        return os.path.basename(filename)

    except requests.HTTPError as he:
        print(f"HTTP error occurred for URL: {url}. Status code: {he.response.status_code}")
    except (requests.RequestException, ValueError):
        print(f"Invalid URL or request failed for URL: {url}")
        with open("failed_requests_pdf_url.txt", "a") as f:
            f.write(url + "\n")

    time.sleep(1)
    return None


def check_doi_exists(doi):
    """Check whether a DOI exists."""
    url = f"https://doi.org/{doi}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.url
        else:
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
