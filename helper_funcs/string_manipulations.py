"""Functions for manipulating strings."""


def create_springer_pdf_urls_from_doi(doi):
    """Return the URL to the PDF of a Springer article."""
    base_url = 'https://link.springer.com/content/pdf/'
    return "".join([base_url, doi, '.pdf'])


def generate_url_to_jstor_pdf(jstor_url):
    """Return the URL to the PDF of a JSTOR article."""
    url_base = 'www.jstor.org/stable/pdf/'
    jstor_id = jstor_url.split('/')[-1]
    return f"{url_base}{jstor_id}.pdf"
