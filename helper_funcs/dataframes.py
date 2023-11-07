import os
from helper_funcs.files import create_filename_with_timestamp


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
    print(f"File: {full_path};\nData shape: {df.shape}")
    return full_path


def find_df_cols_with_less_than_n_unique_values(df, n=3):
    """
    Find columns in a DataFrame with less than `n` unique values.

    Skip columns with list and dict values.
    """
    lst_cols = [col for col in df.columns
                if not df[col].apply(type).eq(list).any()
                if not df[col].apply(type).eq(dict).any()
                and len(df[col].unique()) < n]
    for c in lst_cols:
        print(f"{c}: {df[c].unique()}")
    return lst_cols


def find_df_cols_with_mostly_nans(df, threshold=0.9):
    """Find columns in a DataFrame with mostly NaN values."""
    lst_cols = [col for col in df.columns
                if df[col].isna().sum() / len(df) > threshold]
    print(lst_cols)
    return lst_cols


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
