from pathlib import Path
from typing import Any

from .load_files import base_dir_of, load_file, resolve_ref


def load_columns(filename:str|Path)->dict[str, Any]:
    return resolve_ref(load_file(filename), base_dir_of(filename))
