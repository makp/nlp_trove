"""Functions for working with files."""

import os
import re
from datetime import datetime


def create_filename_with_date(prefix, suffix, extension, timestamp=False):
    """Create a filename with a datestamp."""
    if timestamp:
        today_date = datetime.today().strftime("%m-%d-%y_%H-%M-%S")
    else:
        today_date = datetime.today().strftime("%m-%d-%y")
    filename = f"{prefix}_{today_date}_{suffix}.{extension}"
    print(filename)
    return filename


def find_files_with_filters_and_extensions(
    directory, filter_strs=None, extensions=None
):
    """Find files in directory matching the given filters and extensions."""
    # Ensure that `filter_strs` and `extensions` are lists
    if isinstance(filter_strs, str):
        filter_strs = [filter_strs]
    if isinstance(extensions, str):
        extensions = [extensions]

    # Get all files in the directory
    all_files = os.listdir(directory)

    # Filter files based on `filter_strs` and `extensions`
    filtered_files = (
        file
        for file in all_files
        if (extensions is None or any(file.endswith(ext) for ext in extensions))
        and (
            filter_strs is None
            or any(re.search(filter_str, file) for filter_str in filter_strs)
        )
    )

    # Convert generator to list and sort by creation time
    filtered_files = sorted(
        [os.path.join(directory, file) for file in filtered_files], key=os.path.getctime
    )

    # Print number of files found
    if not filtered_files:
        print("No files found.")
    else:
        print(f"{len(filtered_files)} files found.")

    return filtered_files
