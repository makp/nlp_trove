def extract_jstor_id_from_jstor_url(jstor_url):
    return jstor_url.split('/')[-1]


def generate_jstor_link_to_pdf(jstor_url):
    """"""
    url_base = 'www.jstor.org/stable/pdf/'
    jstor_id = extract_jstor_id_from_jstor_url(jstor_url)
    return f"{url_base}{jstor_id}.pdf"
