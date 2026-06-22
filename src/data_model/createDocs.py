"""Generate Markdown documentation from a loaded database model.

The model is a nested dict (database -> schema -> table -> column/constraint/
index). Two small helpers do the repetitive work:

  * ``_render_table`` turns a list of row-dicts into a Markdown table (or an
    "empty" message), replacing the old per-type print functions.
  * ``_write_page`` creates the parent directory and writes a list of Markdown
    lines, replacing the repeated mkdir/open/write boilerplate.
"""
from pathlib import Path

from py_markdown_table.markdown_table import markdown_table

NO_COMMENT = "No comment present"


def _render_table(rows:dict, keys:list, empty_message:str, emphasise:str=None)->str:
    """_Render a full Markdown table from the set of dict elements._

    Args:
        rows (_type_): _A list of dicts (columns, constraints, indexes, ...)._
        keys (_type_): _The the columns to display, in display order._
        empty_message (_type_): _Text to be returned verbatim when ``rows`` is empty._
        emphasise (_type_, optional): _optional key whose value is wrapped in ``*...*``._ Defaults to None.

    Returns:
        _type_: _description_
    """    

    if not rows:
        return empty_message

    formatted = []
    for row in rows:
        ordered = {key: row.get(key) for key in keys}
        if emphasise is not None:
            ordered[emphasise] = f"*{ordered.get(emphasise)}*"
        formatted.append(ordered)

    try:
        return (
            markdown_table(formatted)
            .set_params(row_sep="markdown", quote=False)
            .get_markdown()
        )
    except Exception:
        print(f"Could not render table for rows: {rows}")
        return ""


def _write_page(path: Path, lines: list) -> None:
    """_Write ``lines`` (one per element) to ``path``, creating parent dirs._

    Args:
        path (Path): _The Path to which the file will be written._
        lines (list): _A list of strings to be written to file._
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def columnPrint(columns:dict)->str:
    """_Provide determininistic column ordering for Markdown._

    Args:
        columns (_dict_): _Taken from the YAML input, a description of the columns (name, type, comment)._

    Returns:
        _str_: _The `columns` section of the markdown page for a table._
    """
    return _render_table(columns, ["name", "type", "comment"], "", emphasise="name")


def constraintPrint(constraints)->str:
    """_Print the `constraints` section of the Markdown pages._

    Args:
        constraints (_dict_): _The dict rendering of the YAML input_

    Returns:
        _str_: _The `constraints` section, with deterministic ordering._
    """    
    return _render_table(
        constraints, ["name", "type", "def", "comment"], "This table has no constraints"
    )


def indexPrint(indices)->str:
    """_Print the `indexes` section of the Markdown pages._
    Args:
        indices (_dict_): _The dict rendering of the YAML input_
    Returns:
        _str_: _The `indexes` section, with deterministic ordering._
    """
    return _render_table(
        indices, ["name", "type", "def", "comment"], "This table has no index"
    )


# --------------------------------------------------------------------------- #
# Page writers
# --------------------------------------------------------------------------- #
def document_database(database: dict, path:Path='docs') -> None:
    """_Renders the documentation from YAML dictionary._

    Args:
        database (dict): _A dict from the composite YAML file._
        path (Path, optional): _Where should the markdown documentation be written?_. Defaults to 'docs'.

    Returns:
        _None_: _Renders the documentation (no object output)._
    """    
    return database_page(database, Path(path) / "database")


def database_page(database: dict, path: Path) -> None:
    lines = [
        f"# {database['name']}",
        f"Description:\n**{database.get('comment', NO_COMMENT)}**",
        "\n## Schemas",
    ]
    for schema in database.get("schema"):
        name = schema.get("name")
        comment = schema.get("comment", NO_COMMENT).strip()
        lines.append(f"* **[{name}](./{name}/{name}.md)**: *{comment}*")
        schema_page(schema, path / name)
    _write_page(path / "index.md", lines)


def schema_page(schema: dict, path: Path) -> None:
    """_Generate the list that renders the `schemas` page._

    Args:
        schema (dict): _The dict object describing the schema._
        path (Path): _The location to which the schema will be sent._
    """    
    name = schema.get("name")
    lines = [
        f"# {name}",
        f"Description:\n**{schema.get('comment', NO_COMMENT).strip()}**",
        "\n## Schema Tables\n",
    ]
    for table in schema.get("tables"):
        if isinstance(table, list):
            lines.append("This schema contains no tables.")
        else:
            lines.append(f"* [{table.get('name')}](tables/{table.get('name')}.md)")
            table_page(table, path / "tables")
    _write_page(path / f"{name}.md", lines)


def table_page(table: dict, path: Path) -> None:
    name = table.get("name")
    lines = [
        f"# {name}",
        f"Description:\n\n**{table.get('comment', NO_COMMENT)}**",
        "\n## Columns\n",
        columnPrint(table.get("columns")),
        "\n## Constraints\n",
        constraintPrint(table.get("constraints", [])),
        "\n## Indexes\n",
        indexPrint(table.get("index", [])),
        "\n## Relationships\n",
    ]
    _write_page(path / f"{name}.md", lines)
