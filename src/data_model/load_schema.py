from .load_files import load_file
from .load_tables import load_tables
from .validate import validate_object
from itertools import chain
from .object_classes import schema_dict

def load_schema(filename:str, validation:dict)->dict:
    schema = load_file(filename)
    valid_schema = validate_object(validation, ddl_object=schema, ddl_type = 'schema')
    
    if 'tables' in valid_schema.keys():
        for i in range(len(valid_schema.get('tables'))):
            if 'ref' in valid_schema.get('tables')[i].keys():
                filename = valid_schema.get('tables')[i].get('ref')
                # This is where we're getting the list inside the list.
                valid_schema.get('tables')[i] = load_tables(filename, validation)
        valid_schema['tables'] = list(chain.from_iterable(valid_schema.get('tables')))
    # Once tables are loaded, we need to make sure that any references mentioned are present.
    return schema_dict(**valid_schema)
