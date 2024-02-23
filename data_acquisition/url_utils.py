"""Misc functions for handling URLs."""

import requests
from bs4 import BeautifulSoup


def find_elements_by_tag_and_attrs(html_content, tag, attr_dict):
    """Find HTML elements based on tag and its attributes."""
    try:
        soup = BeautifulSoup(html_content, 'lxml')
    except Exception as e:
        raise ValueError(f"Error parsing HTML content: {e}")

    found_elements = soup.find_all(tag, attr_dict)
    return found_elements


def fetch_content_from_url(url):
    """
    Fetch content from a given URL.

    Parameters:
    - url (str): The URL from which to fetch the content.

    Returns:
    - str: The content of the fetched URL. None if the request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except (requests.RequestException, ValueError) as e:
        print(f"Invalid URL {url}. Error: {e}")
        with open("failed_requests.txt", "a") as f:
            f.write(url + "\n")


def extract_content_from_url(url, tag, attr_dict):
    """
    Fetch content from a given URL.

    Parameters:
    - url (str): The URL from which to fetch the content.
    - tag (str): The HTML tag to search for within the fetched content.
    - attr_dict (dict): A dictionary containing attribute keys and
      their corresponding values to refine the tag search.

    Returns:
    - str: The content of the 'content' attribute from the found tag
      within the fetched content. If the tag is not found or there's
      an error fetching the content, returns None.

    Side-effects:
    - In case of an invalid URL or request error, the function prints
      an error message and logs the failed URL in a file named
      "failed_requests.txt".
    """
    page_content = fetch_content_from_url(url)
    if page_content:
        return extract_content_from_html(page_content, tag, attr_dict)


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


def create_springer_pdf_urls_from_doi(doi):
    """Return the URL to the PDF of a Springer article."""
    base_url = 'https://link.springer.com/content/pdf/'
    return "".join([base_url, doi, '.pdf'])


def generate_url_to_jstor_pdf(jstor_url):
    """Return the URL to the PDF of a JSTOR article."""
    url_base = 'www.jstor.org/stable/pdf/'
    jstor_id = jstor_url.split('/')[-1]
    return f"{url_base}{jstor_id}.pdf"
