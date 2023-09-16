import pandas as pd


COLUMNS_TO_KEEP_FROM_SPRINGER = [
    'title',
    'creators',
    'publicationName',
    'doi',
    'publicationDate',
    'volume',
    'number',
    'genre',
    'startingPage',
    'endingPage',
    'abstract',
]


def read_articles_from_json(json_path):
    """
    Create a DataFrame from the JSON file downloaded from Springer
    containing the articles' metadata listed in
    `COLUMNS_TO_KEEP_FROM_SPRINGER`.
    """
    df = pd.read_json(json_path)
    df = pd.DataFrame(df['records'].sum())
    return df[COLUMNS_TO_KEEP_FROM_SPRINGER]


def clean_creators(lst_creators):
    """
    Clean the `creators` field.

    The field `creators` is typically a list of dictionaries, where
    each dictionary represents one of the authors. When the JSON file
    is converted into a DataFrame, the articles without a creator have
    value `NaN`.
    """
    if isinstance(lst_creators, list):
        for creator in lst_creators:
            if isinstance(creator, dict) and 'creator' in creator:
                return [creator['creator'] for creator in lst_creators]
    elif pd.isna(lst_creators):
        return pd.NA
    else:
        return lst_creators


def clean_genre(genre):
    """
    Clean the `genre` field.

    The field `genre` can be a string or a list of strings.
    """
    if isinstance(genre, list):
        return genre[0]
    else:
        return genre


def create_springer_pdf_urls_from_doi(doi):
    """Return the Springer URL for the PDF version of an article via
    its DOI."""
    base_url = 'https://link.springer.com/content/pdf/'
    return "".join([base_url, doi, '.pdf'])


def generate_df_from_springer_json(json_path):
    """
    Filter the JSON file to only keep the columns of interest, and
    clean the `creators` and `genre` fields.
    """
    df = read_articles_from_json(json_path)
    df.loc[:, 'creators'] = df['creators'].apply(clean_creators)
    df.loc[:, 'genre'] = df['genre'].apply(clean_genre)
    df['springer_url'] = df['doi'].apply(create_springer_pdf_urls_from_doi)
    for col in df.columns:
        data_type = df[col].apply(type).unique()
        print(f"{col}: {data_type}")
    return df
