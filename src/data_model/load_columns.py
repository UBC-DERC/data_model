from pathlib import Path
from typing import Any

from .load_files import base_dir_of, load_file, resolve_ref


def load_columns(filename:str|Path)->dict[str, Any]:
    """_Load column data from a given reference_

    Args:
        filename (str | Path): _A Path object or string pointing to a file._

    Returns:
        dict[str, Any]: _Returns a dictionary containing the loaded column data._
    """
    return resolve_ref(load_file(filename), base_dir_of(filename))
