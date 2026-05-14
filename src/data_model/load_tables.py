from .load_files import load_file
from .validate import validate_object
from .load_columns import load_columns

def load_tables(filename:str, validation:dict)->dict:
    tables = load_file(filename)
    if type(tables) is list:
        valid_table = []
        for i in range(len(tables)):
            tester = validate_object(validation, ddl_object=tables[i], ddl_type = 'table')
            if 'columns' in tester.keys():
                for i in range(len(tester.get('columns'))):
                    if 'ref' in tester.get('columns')[i].keys():
                        filename = tester.get('columns')[i].get('ref')
                        tester.get('columns')[i] = load_columns(filename, validation)   
    else:
        valid_table = validate_object(validation, ddl_object=tables, ddl_type = 'table')
    return valid_table
