from .load_files import load_file
from .load_schema import load_schema
from .validate import validate_object
from .object_classes import DDL_Dict

def load_database(filename:str, validation:dict)->dict:
    """_Recursively load the database model from an existing YAML file._

    Args:
        filename (str): _A valid filename pointing to a YAML database definition file._
        validation (dict): _A dict object that defines the allowed fields for any type of object to assist with rendering._

    Returns:
        dict: _A dict object (that can be serialized to YAML) representing the fully described database model._
    """
    db = load_file(filename)
    validate_object(validation, ddl_object = db, ddl_type = 'database')
    print('Database object okay!')

    if 'schemas' in db.keys():
        for i in range(len(db.get('schemas'))):
            filename = db.get('schemas')[i].get('ref')
            db.get('schemas')[i] = load_schema(filename, validation)
    return DDL_Dict(**db)
