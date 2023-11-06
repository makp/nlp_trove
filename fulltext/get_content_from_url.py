import requests
from bs4 import BeautifulSoup


def extract_content_from_html(html_content, tag, attr_dict):
    """
    Extracts content from given HTML based on tag and its attributes.

    Parameters:
    - html_content (str): The HTML content as a string.
    - tag (str): The HTML tag to search for.
    - attr_dict (dict): A dictionary containing attribute keys and
      their corresponding values to refine the tag search.

    Returns:
    - str: The content of the 'content' attribute from the found tag.
      If the tag is not found, returns None.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    meta_tag = soup.find(tag, attr_dict)
    if meta_tag:
        return meta_tag['content']
    else:
        return None


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
    Fetches content from a given URL.

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
