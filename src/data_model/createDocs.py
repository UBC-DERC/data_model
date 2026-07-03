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


def _reference_link(current_schema:str, target_schema:str, target_table:str)->str:
    """_Build a Markdown link to a referenced table's documentation page._

    Table pages live at ``<schema>/tables/<table>.md``. A same-schema target is
    a sibling page; a cross-schema target is reached by walking up to the
    ``database`` folder and back down into the other schema.
    """
    if target_schema == current_schema:
        path = f"{target_table}.md"
    else:
        path = f"../../{target_schema}/tables/{target_table}.md"
    return f"[{target_table}]({path})"


def build_incoming_index(database)->dict:
    """_Map each referenced ``(schema, table)`` to the foreign keys that target it._

    Args:
        database: _A loaded, reference-resolved database model._

    Returns:
        dict: _``(schema, table) -> [{schema, table, columns, target_columns}]``,
            one entry per incoming foreign key. Tables with no incoming
            references are absent from the mapping._
    """
    index:dict = {}
    for schema in database.schemas:
        for table in schema.tables:
            for constraint in table.constraints:
                ref = constraint.references
                if ref is None:
                    continue
                index.setdefault((ref.schema_, ref.table), []).append({
                    "schema": schema.name,
                    "table": table.name,
                    "columns": list(constraint.columns),
                    "target_columns": list(ref.columns),
                })
    return index


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
        ordered = {key: getattr(row, key) for key in keys}
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
        constraints, ["name", "type", "ddl", "comment"], "This table has no constraints"
    )


def indexPrint(indices)->str:
    """_Print the `indexes` section of the Markdown pages._
    Args:
        indices (_dict_): _The dict rendering of the YAML input_
    Returns:
        _str_: _The `indexes` section, with deterministic ordering._
    """
    return _render_table(
        indices, ["name", "type", "ddl", "comment"], "This table has no index"
    )


# --------------------------------------------------------------------------- #
# Page metadata
# --------------------------------------------------------------------------- #
def _front_matter(title: str, description: str) -> str:
    """Build a YAML front-matter block with a page title and meta description.

    The description is whitespace-collapsed, truncated to a search-engine
    friendly length (~160 chars), and double-quotes are escaped so the YAML
    stays valid. MkDocs/Material expose these via ``page.title`` and
    ``page.meta.description`` (used for per-page ``<meta>`` and Open Graph tags).
    """
    text = " ".join((description or NO_COMMENT).split())
    if len(text) > 160:
        text = text[:157].rstrip() + "..."
    title = title.replace('"', '\\"')
    text = text.replace('"', '\\"')
    return f'---\ntitle: "{title}"\ndescription: "{text}"\n---\n'


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
        _front_matter(
            f"{database.name} database", database.comment
        ),
        f"# {database.name}",
        f"Description:\n**{database.comment}**",
        "\n## Schemas",
    ]
    for schema in database.schemas:
        name = schema.name
        comment = schema.comment.strip()
        lines.append(f"* **[{name}](./{name}/index.md)**: *{comment}*")
        schema_page(schema, path / name)
    _write_page(path / "index.md", lines)


def schema_page(schema: dict, path: Path) -> None:
    """_Generate the list that renders the `schemas` page._

    Args:
        schema (dict): _The dict object describing the schema._
        path (Path): _The location to which the schema will be sent._
    """    
    name = schema.name
    lines = [
        _front_matter(f"The {name} schema", schema.comment),
        f"# `{name}` Schema",
        f"Description:\n**{schema.comment.strip()}**",
        "\n## Tables\n",
    ]
    for table in schema.tables:
        if isinstance(table, list):
            lines.append("This schema contains no tables.")
        else:
            lines.append(f"* [{table.name}](tables/{table.name}.md)")
            table_page(table, path / "tables")
    # Write the schema page as the folder's index page so MkDocs (with the
    # navigation.indexes feature) collapses the "<schema>/" section and its
    # landing page into a single nav entry instead of a folder + child page.
    _write_page(path / "index.md", lines)


def table_page(table: dict, path: Path) -> None:
    name = table.name
    lines = [
        _front_matter(f"{name} table", table.comment),
        f"# {name}",
        f"Description:\n\n**{table.comment}**",
        "\n## Columns\n",
        columnPrint(table.columns),
        "\n## Constraints\n",
        constraintPrint(table.constraints),
        "\n## Indexes\n",
        indexPrint(table.indexes),
        "\n## Relationships\n",
    ]
    _write_page(path / f"{name}.md", lines)
