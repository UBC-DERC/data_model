from .check_references import check_references
from .load_files import load_file, resolve_ref
from .load_schema import load_schema
from .object_classes import DDL_Dict


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
    db = resolve_ref(load_file(filename))
    if "schemas" in db:
        db["schemas"] = [load_schema(s["ref"]) for s in db["schemas"]]
    database = DDL_Dict(**db)
    check_references(database)
    return database
