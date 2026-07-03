from .load_files import load_file, resolve_ref
from .load_columns import load_columns


def load_tables(filename:str)->list | dict:
    tables = load_file(filename)
    if isinstance(tables, list):
        result = []
        for table in tables:
            table = resolve_ref(table)
            if "columns" in table:
                table["columns"] = [
                    load_columns(c["ref"]) if "ref" in c else c
                    for c in table["columns"]
                ]
            result.append(table)
        return result
    return resolve_ref(tables)
