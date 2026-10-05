from typing import Any

from .check_crossreferences import check_references
from .load_files import base_dir_of, load_file, resolve_ref
from .load_schema import load_schema
from .object_classes import DDL_Dict


def load_database(filename:str)->DDL_Dict:
    """Recursively load and validate the database model from a YAML entry file.

    The model is assembled from the entry file and its ``$ref:`` targets, built
    into Pydantic models (structural validation). The loading module loads all objects
    and then checks for unresolved references across all schemas and tables at the
    end, to simplify the loading flow.

    Args:
        filename (str): Path to the database entry YAML file.

    Returns:
        DDL_Dict: The validated, reference-checked database model.
    """
    base = base_dir_of(filename)
    file = load_file(filename)
    db: dict[str, Any] = resolve_ref(file, base)
    db_slug: dict[str, Any] | None = db.get('database', None)
    if db_slug is None:
      # There's no database block in the entry file, so we can't load a database model.
      # This should be an error.
      raise ValueError(
                  f"database entry file {filename!r} has no 'database:' block; "
                  "cannot load database model."
      )
    db_slug["schemas"] = [
        load_schema(base / s["$ref"]) if "$ref" in s else s
        for s in db_slug["schemas"]
    ]
    database = DDL_Dict(**db_slug)
    check_references(database)
    return database
