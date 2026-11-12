"""Generate the JSON Schema for ddlml documents from the Pydantic models.

The schema is derived from the :class:`~data_model.object_classes.ddlml_dict`, so it
always matches the models used for validation. It is published alongside the
documentation at :data:`SCHEMA_URL` (see ``hooks/json_schema.py``, which runs
this on every ``mkdocs build``/``serve``).

The goal is to have an available JSON schema for ddlml documents, so that they can be validated in editors and IDEs.

TODO: Note that the schema only works with complete ddlml documents, so it's not entirely user friendly
yet when building documents with ``$ref`` tags.
"""

import json
from pathlib import Path
from typing import Any

from .object_classes import ddlml_dict

SCHEMA_URL = "https://ubc-derc.github.io/ddlml/schema.json"
JSON_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"


def build_schema() -> dict[str, Any]:
    """Build the JSON Schema for a ddlml document.

    Returns:
        dict: The JSON Schema, with ``$schema`` and ``$id`` set.
    """
    schema = ddlml_dict.model_json_schema()
    return {"$schema": JSON_SCHEMA_DIALECT, "$id": SCHEMA_URL, **schema}


def schema_json() -> str:
    """Return the JSON Schema serialised as an indented JSON string."""
    return json.dumps(build_schema(), indent=2) + "\n"


def write_schema(path: str | Path) -> Path:
    """Write the JSON Schema to ``path``, creating parent directories.

    Args:
        path (str | Path): Destination file.

    Returns:
        Path: The path written to.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(schema_json())
    return path
