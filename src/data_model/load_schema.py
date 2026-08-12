from itertools import chain

from .load_files import load_file, resolve_ref, base_dir_of
from .load_tables import load_tables
from .model_build import build_tables
from .object_classes import schema_dict


def load_schema(filename:str)->schema_dict:
    base = base_dir_of(filename)
    schema = resolve_ref(load_file(filename), base)
    if "tables" in schema:
        for i in range(len(schema["tables"])):
            if "ref" in schema["tables"][i]:
                # Table refs resolve relative to the schema file's directory.
                schema["tables"][i] = load_tables(base / schema["tables"][i]["ref"])
        schema["tables"] = list(chain.from_iterable(schema["tables"]))
        # Build each table individually so structural problems are reported with
        # clear, table- and constraint-scoped messages (see model_build).
        schema["tables"] = build_tables(schema["tables"])
    # Cross-reference checks run later, once the whole database is assembled.
    return schema_dict(**schema)
