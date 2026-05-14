from .load_files import load_file
from .validate import validate_object

def load_columns(filename:str, validation:dict)->dict:
    columns = load_file(filename)
    valid_column = validate_object(validation, ddl_object=columns, ddl_type = 'column')
    return valid_column
