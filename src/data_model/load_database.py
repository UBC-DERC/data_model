from .load_files import load_file, resolve_ref, base_dir_of
from .load_schema import load_schema
from .object_classes import DDL_Dict
from .check_crossreferences import check_references


def load_database(filename:str)->DDL_Dict:
    """_Recursively load and validate the database model from a YAML entry file._

    The model is assembled from the entry file and its ``ref:`` targets, built
    into pydantic models (structural validation), then checked for unresolved
    references across all schemas and tables.

    Args:
        filename (str): _Path to the database entry YAML file._

    Returns:
        DDL_Dict: _The validated, reference-checked database model._
    """
    base = base_dir_of(filename)
    file = load_file(filename)
    db = resolve_ref(file, base)
    if db.get('schemas', None):
        # Schemas may arrive two ways: as ``ref:`` pointers that must be loaded
        # and assembled from component files, or as fully-inlined schema dicts
        # (e.g. a serialised model like tests/samples/output.yaml). Resolve each
        # entry independently and leave inline schemas for DDL_Dict to validate.
        # Refs are resolved relative to the entry file's directory.
        db["schemas"] = [
            load_schema(base / s["ref"]) if "ref" in s else s
            for s in db["schemas"]
        ]
    database = DDL_Dict(**db)
    check_references(database)
    return database
