def validate_table(schema:dict, ddl_object:dict, type:str="table")->dict:
    keys = ddl_object.keys()
    