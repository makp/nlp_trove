import pandas as pd


def clean_creators(creators):
    """
    Clean the `creators` field.

    The field `creators` is typically a list of dictionaries, where
    each dictionary represents one of the authors. When the JSON file
    is converted into a DataFrame, the articles without a creator have
    value `NaN`.
    """
    if isinstance(creators, list):
        for creator in creators:
            if isinstance(creator, dict) and 'creator' in creator:
                return [creator['creator'] for creator in creators]
    elif pd.isna(creators):
        return pd.NA
    else:                       # creators are neither a list nor NaN
        return creators


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
