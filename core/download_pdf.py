import requests
import time
import os
import hashlib


def download_pdf_from_url(url, headers=None, output_dir=''):
    if headers is None:
        headers = {}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        content_type = response.headers.get("content-type", '')
        if 'application/pdf' not in content_type:
            # print(f"The URL: {url} was redirected to an unexpected page.")
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
