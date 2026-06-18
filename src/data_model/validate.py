from .load_files import load_file

def validate_object(schema:dict, ddl_object:dict, ddl_type:str="table")->dict:
    keys = ddl_object.keys()
    if 'ref' in keys:
        yamlFile = load_file(ddl_object.get('ref'))
        ddl_object = ddl_object | yamlFile
    withRefs = schema.get(ddl_type).get('keys') + ['ref']
    extra = [i for i in keys if i not in withRefs]
    assert len(extra) == 0, f"There are extra fields in your definition file: {extra}"
    return ddl_object
