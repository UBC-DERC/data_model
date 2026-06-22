"""Tests for data_model.createDocs (Markdown generation).

These cover the small formatting helpers (``columnPrint`` / ``constraintPrint``
/ ``indexPrint`` / ``columnFormatter``) and the page writers
(``table_page`` / ``schema_page`` / ``database_page`` / ``document_database``).

A few tests pin down known quirks:
  * ``columnFormatter`` mutates its input list in place;
  * ``constraintPrint``/``indexPrint`` read the ``def`` key, while the data and
    validation.yaml use ``definition``;
  * ``table_page`` reads ``table['index']`` while the schema key is ``indexes``;
  * ``document_database`` ignores its ``path`` argument and always writes to
    ``./docs/``.
"""
from data_model import document_database
from data_model.createDocs import (
    columnPrint,
    constraintPrint,
    database_page,
    indexPrint,
    schema_page,
    table_page,
)


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def test_column_print_renders_all_columns():
    cols = [
        {"name": "cadid", "type": "text", "comment": "id"},
        {"name": "gender", "type": "nchar(1)", "comment": "g"},
    ]
    out = columnPrint(cols)
    # Names are emphasised with surrounding asterisks.
    assert "*cadid*" in out
    assert "*gender*" in out
    assert "text" in out
    assert "nchar(1)" in out


def test_constraint_print_empty():
    assert constraintPrint([]) == "This table has no constraints"


def test_index_print_empty():
    assert indexPrint([]) == "This table has no index"


def test_constraint_print_reads_def_key():
    """constraintPrint reads 'def' (not 'definition')."""
    rendered = constraintPrint(
        [{"name": "pk", "type": "PRIMARY KEY", "def": "PRIMARY KEY (cadid)", "comment": "c"}]
    )
    assert "PRIMARY KEY (cadid)" in rendered


def test_constraint_print_ignores_definition_key():
    """Known mismatch: data uses 'definition', renderer reads 'def'.

    The definition text is therefore dropped from the output. Update this
    test once the renderer/schema are reconciled on a single key name.
    """
    rendered = constraintPrint(
        [{"name": "pk", "type": "PRIMARY KEY", "definition": "PRIMARY KEY (cadid)"}]
    )
    assert "PRIMARY KEY (cadid)" not in rendered


# --------------------------------------------------------------------------- #
# Page writers
# --------------------------------------------------------------------------- #
def _sample_table():
    return {
        "name": "cows",
        "comment": "cow table",
        "columns": [{"name": "cadid", "type": "text", "comment": "id"}],
        "constraints": [
            {"name": "pk", "type": "PRIMARY KEY", "def": "PRIMARY KEY (cadid)", "comment": "c"}
        ],
    }


def test_table_page_writes_markdown(tmp_path):
    table_page(_sample_table(), tmp_path / "tables")
    out = tmp_path / "tables" / "cows.md"
    assert out.is_file()
    text = out.read_text()
    assert "# cows" in text
    assert "## Columns" in text
    assert "*cadid*" in text
    assert "## Constraints" in text
    assert "PRIMARY KEY (cadid)" in text
    assert "## Indexes" in text
    assert "## Relationships" in text


def test_table_page_falls_back_when_no_constraints(tmp_path):
    table = {"name": "bare", "comment": "x", "columns": [{"name": "c", "type": "text", "comment": ""}]}
    table_page(table, tmp_path / "tables")
    text = (tmp_path / "tables" / "bare.md").read_text()
    assert "This table has no constraints" in text
    assert "This table has no index" in text


def test_schema_page_writes_schema_and_tables(tmp_path):
    schema = {
        "name": "dairy",
        "comment": "the dairy schema",
        "tables": [_sample_table()],
    }
    schema_page(schema, tmp_path / "dairy")
    schema_md = tmp_path / "dairy" / "dairy.md"
    assert schema_md.is_file()
    text = schema_md.read_text()
    assert "# dairy" in text
    assert "[cows](tables/cows.md)" in text
    # The per-table page was generated too.
    assert (tmp_path / "dairy" / "tables" / "cows.md").is_file()


def test_database_page_writes_index_and_schemas(tmp_path):
    database = {
        "name": "dairymodel",
        "comment": "the whole db",
        "schema": [
            {"name": "dairy", "comment": "dairy schema", "tables": [_sample_table()]},
        ],
    }
    database_page(database, tmp_path / "database")
    index = tmp_path / "database" / "index.md"
    assert index.is_file()
    text = index.read_text()
    assert "# dairymodel" in text
    assert "[dairy](./dairy/dairy.md)" in text
    assert (tmp_path / "database" / "dairy" / "dairy.md").is_file()


def test_document_database_ignores_path_and_uses_cwd_docs(tmp_path, monkeypatch):
    """document_database hardcodes ``Path('docs/')`` and ignores its argument.

    By running it inside a temp cwd we can assert the output lands in
    ``<cwd>/docs/database`` regardless of the path we pass in.

    Note: the page writers use ``path.mkdir()`` without ``parents=True``,
    so ``docs/`` must already exist (as it does in the real repo). We
    create it here to mirror that precondition.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / "docs").mkdir()
    database = {
        "name": "dairymodel",
        "comment": "db",
        "schema": [{"name": "dairy", "comment": "s", "tables": [_sample_table()]}],
    }
    # Pass an unrelated path to prove it is ignored.
    document_database(database, tmp_path / "ignored_output_dir")

    assert (tmp_path / "docs" / "database" / "index.md").is_file()
    assert not (tmp_path / "ignored_output_dir").exists()
