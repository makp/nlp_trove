import pandas as pd


def extract_jstor_id_from_jstor_url(jstor_url):
    return jstor_url.split('/')[-1]


def generate_jstor_link_to_pdf(jstor_url):
    """"""
    url_base = 'www.jstor.org/stable/pdf/'
    jstor_id = extract_jstor_id_from_jstor_url(jstor_url)
    return f"{url_base}{jstor_id}.pdf"


def are_jstor_articles_in_main_df(df, df_jstor,
                                  columns=['title', 'title']):
    """
    Check if all articles in df_jstor are present in df based on a
    specified column.
    """
    if columns[0] not in df.columns or columns[1] not in df_jstor.columns:
        return "Invalid column names"

    merged_df = pd.merge(df, df_jstor,
                         left_on=columns[0],
                         right_on=columns[1],
                         how='inner')
    if len(merged_df) == len(df_jstor):
        return True
    else:
        missing_articles = len(df_jstor) - len(merged_df)
        print(f"{missing_articles} articles not present in the main DataFrame")
        return False
