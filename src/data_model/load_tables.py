from .load_columns import load_columns
from .load_files import base_dir_of, load_file, resolve_ref


def load_tables(filename:str)->list | dict:
    # ``filename`` may be a single tables file or a directory of table files;
    # base_dir_of handles both so refs resolve relative to the right location.
    base = base_dir_of(filename)
    tables = load_file(filename)
    if isinstance(tables, list):
        result = []
        for table in tables:
            table = resolve_ref(table, base)
            if "columns" in table:
                table["columns"] = [
                    load_columns(base / c["ref"]) if "ref" in c else c
                    for c in table["columns"]
                ]
            result.append(table)
        return result
    return resolve_ref(tables, base)
