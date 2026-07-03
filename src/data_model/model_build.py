"""Build pydantic models from validated YAML dicts with clear error messages.

Constructing ``table_dict`` directly raises pydantic ``ValidationError``s whose
locations are numeric paths (``constraints.2.references``). For a tool aimed at
users who are not SQL or pydantic experts, those are hard to act on. This
module builds each table individually, translates every validation problem into
a sentence that names the table, the constraint (by name, not index), the
field, and the offending value, and reports every bad table together so a
maintainer can fix them all in one pass.
"""
from pydantic import ValidationError

from .object_classes import table_dict


class ModelValidationError(Exception):
    """Raised when one or more table definitions fail structural validation."""


def _label_location(data: dict, loc: tuple) -> str:
    """Render a pydantic error location using item names instead of indices.

    Walks ``loc`` against the original input ``data`` so that a list index is
    shown as the named item it points at (e.g. a constraint's ``name``) rather
    than a bare number.
    """
    parts: list[str] = []
    node = data
    for key in loc:
        if isinstance(key, int):
            item = node[key] if isinstance(node, list) and key < len(node) else None
            if isinstance(item, dict) and "name" in item:
                parts.append(f"'{item['name']}'")
            else:
                parts.append(f"[{key}]")
            node = item
        else:
            parts.append(str(key))
            node = node.get(key) if isinstance(node, dict) else None
    return " -> ".join(parts) if parts else "(table)"


def _describe_errors(data: dict, error: ValidationError) -> list[str]:
    """Turn one table's ValidationError into readable, table-scoped messages."""
    table_name = data.get("name", "(unnamed table)")
    messages: list[str] = []
    for err in error.errors():
        where = _label_location(data, err["loc"])
        messages.append(f"table '{table_name}' {where}: {err['msg']}")
    return messages


def build_tables(table_dicts: list[dict]) -> list[table_dict]:
    """Build ``table_dict`` models from validated dicts, or report all problems.

    Args:
        table_dicts (list[dict]): _Per-table dicts, with any ``ref:`` targets
            already merged._

    Returns:
        list[table_dict]: _The built models, in input order._

    Raises:
        ModelValidationError: _If any table fails structural validation; the
            message lists every problem, one per line._
    """
    built: list[table_dict] = []
    problems: list[str] = []
    for data in table_dicts:
        try:
            built.append(table_dict(**data))
        except ValidationError as error:
            problems.extend(_describe_errors(data, error))
    if problems:
        raise ModelValidationError(
            "Problems found in table definitions:\n  - " + "\n  - ".join(problems)
        )
    return built
