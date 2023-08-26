import requests
from bs4 import BeautifulSoup
# import logging


def extract_pdf_url_from_doi_html(html_content, tag, attr_dict):
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_tag = soup.find(tag, attr_dict)
    if meta_tag:
        return meta_tag['content']
    else:
        return None


def get_pdf_url_from_doi_url(doi_url, tag, attr_dict):
    try:
        response = requests.get(doi_url)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        print(f"Invalid DOI or request failed for DOI URL: {doi_url}")
        with open("failed_doi_requests.txt", "a") as f:
            f.write(doi_url + "\n")
        return
    page_content = response.text
    return extract_pdf_url_from_doi_html(page_content, tag, attr_dict)
