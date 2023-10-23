import pandas as pd


TRANSLATION_MAP_FOR_SCOPUS = {
    'dc:identifier': 'sc_id',
    'dc:title': 'sc_title',
    'dc:creator': 'sc_creator',
    'prism:volume': 'sc_volume',
    'prism:issueIdentifier': 'sc_issue',
    'prism:pageRange': 'sc_pageRange',
    'prism:coverDate': 'sc_date',
    'prism:doi': 'sc_doi',
    'citedby-count': 'sc_citedby-count',
    'affiliation': 'sc_affiliation',
    'subtypeDescription': 'sc_subtype',
    'article-number': 'sc_article-number'}


def read_articles_from_scopus_json(json_path):
    """
    Create a DataFrame from the JSON file downloaded from Scopus and
    filter the records acconding to `TRANSLATION_MAP_FOR_SCOPUS`.
    """
    df = pd.read_json(json_path)
    df = df[list(TRANSLATION_MAP_FOR_SCOPUS.keys())]
    df = df.rename(columns=TRANSLATION_MAP_FOR_SCOPUS)
    return df


def generate_df_from_scopus_json(json_path):
    """
    Filter the JSON file downloaded from Scopus according to
    `TRANSLATION_MAP_FOR_SCOPUS` and change the data types of some
    columns.
    """
    df = read_articles_from_scopus_json(json_path)
    df['sc_date'] = pd.to_datetime(df['sc_date'])
    na_doi = df['sc_doi'].isna()
    if na_doi.any():
        print(f"Warning: {na_doi.sum()} article(s) lack a DOI")
    for column in df.columns:
        print(f"{column}: {df[column].apply(type).unique()}")
    return df
