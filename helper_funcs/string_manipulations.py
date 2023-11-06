"""
This module contains functions for manipulating strings.
"""


def create_springer_pdf_urls_from_doi(doi):
    """Return the Springer URL for the PDF version of an article via
    its DOI."""
    base_url = 'https://link.springer.com/content/pdf/'
    return "".join([base_url, doi, '.pdf'])


def generate_url_to_jstor_pdf(jstor_url):
    url_base = 'www.jstor.org/stable/pdf/'
    jstor_id = jstor_url.split('/')[-1]
    return f"{url_base}{jstor_id}.pdf"
