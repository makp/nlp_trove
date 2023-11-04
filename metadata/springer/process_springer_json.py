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

    The field `genre` can be a string or a list of strings. When
    `genre` is a list, the first element is the general genre, and the
    second element contains more specific information (e.g., name of
    the special issue).
    """
    if isinstance(genre, list):
        # return ', '.join(genre)
        return genre[0]
    else:
        return genre




def generate_df_from_springer_json(json_path):
    """
    Filter the JSON file to only keep the columns of interest, clean
    the `creators` and `genre` fields, and change the data types of
    some columns.
    """
    df = read_articles_from_json(json_path)
    df['publicationDate'] = pd.to_datetime(df['publicationDate'])
    df['creators'] = df['creators'].apply(clean_creators)
    df['genre'] = df['genre'].apply(clean_genre)
    df['startingPage'] = pd.to_numeric(df['startingPage'], errors='coerce')
    df['endingPage'] = pd.to_numeric(df['endingPage'], errors='coerce')
    df['num_pages'] = df['endingPage'] - df['startingPage'] + 1
    # df['springer_url'] = df['doi'].apply(create_springer_pdf_urls_from_doi)
    print("Column data types:")
    for col in df.columns:
        data_type = df[col].apply(type).unique()
        print(f"{col}: {data_type}")
    return df
