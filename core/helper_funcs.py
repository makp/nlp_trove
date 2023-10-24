import os
from datetime import datetime


def save_df(df, folder_path, prefix='out', suffix='', extension='pkl'):
    """Save a DataFrame to a file."""
    today_date = datetime.today().strftime('%m-%d-%y_%H-%M-%S')
    if suffix:
        filename = f"{prefix}_{today_date}_{suffix}.{extension}"
    else:
        filename = f"{prefix}_{today_date}.{extension}"

    full_path = os.path.join(folder_path, filename)

    method_map = {
        'csv': ('to_csv', 'index=False'),
        'pkl': ('to_pickle', None),
    }
    method_name, kwargs = method_map[extension]
    getattr(df, method_name)(full_path, kwargs)
    return print(f"File: {full_path};\nData shape: {df.shape}")


def find_database_file(database_dir, filter_str=None, extension='pkl'):
    files = [f for f in os.listdir(database_dir) if f.endswith(extension)]
    if filter_str:
        files = [f for f in files if filter_str in f]

    if not files:
        return None

    print(f"Found {len(files)} files")

    files = [os.path.join(database_dir, f) for f in files]
    return sorted(files, key=os.path.getctime)
