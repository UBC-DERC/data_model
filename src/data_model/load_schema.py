from itertools import chain

from .load_files import load_file, resolve_ref
from .load_tables import load_tables
from .object_classes import schema_dict
from .model_build import build_tables


def load_schema(filename:str)->schema_dict:
    schema = resolve_ref(load_file(filename))
    if "tables" in schema:
        for i in range(len(schema["tables"])):
            if "ref" in schema["tables"][i]:
                schema["tables"][i] = load_tables(schema["tables"][i]["ref"])
        schema["tables"] = list(chain.from_iterable(schema["tables"]))
        # Build each table individually so structural problems are reported with
        # clear, table- and constraint-scoped messages (see model_build).
        schema["tables"] = build_tables(schema["tables"])
    # Cross-reference checks run later, once the whole database is assembled.
    return schema_dict(**schema)
