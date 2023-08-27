import requests
from bs4 import BeautifulSoup


def extract_content_from_html(html_content, tag, attr_dict):
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_tag = soup.find(tag, attr_dict)
    if meta_tag:
        return meta_tag['content']
    else:
        return None


def extract_content_from_url(url, tag, attr_dict):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        print(f"Invalid URL: {url}")
        with open("failed_requests.txt", "a") as f:
            f.write(url + "\n")
        return
    page_content = response.text
    return extract_content_from_html(page_content, tag, attr_dict)
