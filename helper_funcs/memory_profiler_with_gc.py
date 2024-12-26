"""
Use garbage collection to analyze memory usage.

These functions might be be useful for tracking memory spikes in the code.
"""

import gc
from collections import Counter


def count_num_objects_by_type():
    """Analyze memory usage by counting number of objects in memory."""
    type_count = Counter(type(o).__name__ for o in gc.get_objects())
    return dict(type_count.most_common(10))


def count_num_objects():
    gc.collect()  # Force garbage collection before counting objects
    num_objs = len(gc.get_objects())
    return num_objs
