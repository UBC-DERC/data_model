from pathlib import Path
from typing import Any

from .load_files import base_dir_of, load_file, resolve_ref


def load_columns(filename:str|Path)->dict[str, Any]:
    """Load column data from a given reference

    Args:
        filename (str | Path): A Path object or string pointing to a file.

    Returns:
        dict[str, Any]: Returns a dictionary containing the loaded column data.
    """
    return resolve_ref(load_file(filename), base_dir_of(filename))
