import os
from datetime import datetime


def create_filename_with_timestamp(prefix, suffix, extension):
    """Create a filename with a timestamp."""
    today_date = datetime.today().strftime('%m-%d-%y_%H-%M-%S')
    if suffix:
        filename = f"{prefix}_{today_date}_{suffix}.{extension}"
    else:
        filename = f"{prefix}_{today_date}.{extension}"
    return filename


def save_df(df, folder_path, prefix='out', suffix='', extension='pkl'):
    """Save a DataFrame to a file."""
    filename = create_filename_with_timestamp(prefix, suffix, extension)

    full_path = os.path.join(folder_path, filename)

    method_map = {
        'csv': ('to_csv', 'index=False'),
        'pkl': ('to_pickle', None),
    }
    method_name, kwargs = method_map[extension]
    getattr(df, method_name)(full_path, kwargs)
    return print(f"File: {full_path};\nData shape: {df.shape}")


def create_springer_pdf_urls_from_doi(doi):
    """Return the Springer URL for the PDF version of an article via
    its DOI."""
    base_url = 'https://link.springer.com/content/pdf/'
    return "".join([base_url, doi, '.pdf'])


def generate_url_to_jstor_pdf(jstor_url):
    url_base = 'www.jstor.org/stable/pdf/'
    jstor_id = jstor_url.split('/')[-1]
    return f"{url_base}{jstor_id}.pdf"


def find_database_file(database_dir, filter_str=None, extension='pkl'):
    files = [f for f in os.listdir(database_dir) if f.endswith(extension)]
    if filter_str:
        files = [f for f in files if filter_str in f]

    if not files:
        return None

    print(f"Found {len(files)} files")

    files = [os.path.join(database_dir, f) for f in files]
    return sorted(files, key=os.path.getctime)


# def are_jstor_articles_in_main_df(df, df_jstor,
#                                   columns=['title', 'title']):
#     """
#     Check if all articles in df_jstor are present in df based on a
#     specified column.
#     """
#     if columns[0] not in df.columns or columns[1] not in df_jstor.columns:
#         return "Invalid column names"

#     merged_df = pd.merge(df, df_jstor,
#                          left_on=columns[0],
#                          right_on=columns[1],
#                          how='inner')
#     if len(merged_df) == len(df_jstor):
#         return True
#     else:
#         missing_articles = len(df_jstor) - len(merged_df)
#         print(f"{missing_articles} articles not present in the main DataFrame")
#         return False


# def only_in_df_jstor(df, df_jstor, column='title'):
#     merged_df = pd.merge(df, df_jstor, on=column, how='outer',
#                          indicator="origin")
#     only_in_df_jstor = merged_df[merged_df['origin'] == "right_only"]
#     return only_in_df_jstor.drop('origin', axis=1)
