import pandas as pd
import json


def convert_record_to_dict(record):
    record_dict = {
        "contentType": record.get("contentType", None),
        "genre": ', '.join(record.get("genre", [])),
        "journal": record.get("publicationName", None),
        "author": ', '.join([d['creator']
                             for d in record.get('creators', [])]),
        "title": record.get('title', None),
        "abstract": record.get("abstract", None),
        "publicationDate": record.get("publicationDate", None),
        "doi": record.get("doi", None)
        }
    return record_dict


def filter_all_records(json_path):
    with open(json_path) as f:
        data = json.load(f)
    data_list = []
    for response in data:
        for record in response["records"]:
            record_dict = convert_record_to_dict(record)
            data_list.append(record_dict)
    return pd.DataFrame(data_list)


def create_springer_pdf_urls_from_doi(doi):
    """Return the Springer URL for the PDF version of an article via
    its DOI."""
    base_url = 'https://link.springer.com/content/pdf/'
    return "".join([base_url, doi, '.pdf'])
