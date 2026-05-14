from .load_files import load_file
from .load_tables import load_tables
from .validate import validate_object

def load_schema(filename:str, validation:dict)->dict:
    schema = load_file(filename)
    valid_schema = validate_object(validation, ddl_object=schema, ddl_type = 'schema')
    
    if 'tables' in valid_schema.keys():
        for i in range(len(valid_schema.get('tables'))):
            if 'ref' in valid_schema.get('tables')[i].keys(): 
                filename = valid_schema.get('tables')[i].get('ref')
                valid_schema.get('tables')[i] = load_tables(filename, validation)

    return valid_schema
