"""Tests for data_model.createDocs (Markdown generation).

The renderers consume the pydantic model objects produced by the loader
(``table_dict``/``schema_dict``/``DDL_Dict`` etc.), reading attributes such as
``.name`` and ``.columns``. These tests build those objects and assert the
current behaviour: constraints/indexes render their ``ddl``, and the page
writers honour the ``path`` they are given.
"""
from data_model import document_database
from data_model.createDocs import (
    _reference_link,
    build_incoming_index,
    columnPrint,
    constraintPrint,
    database_page,
    indexPrint,
    schema_page,
    table_page,
)
from data_model.object_classes import (
    DDL_Dict,
    column_dict,
    constraint_dict,
    index_dict,
    reference_dict,
    schema_dict,
    table_dict,
)


def test_reference_link_same_schema():
    assert _reference_link("dairy", "dairy", "institutions") == "[institutions](institutions.md)"


def test_reference_link_cross_schema():
    assert _reference_link("dairy", "apps", "logs") == "[logs](../../apps/tables/logs.md)"


def test_build_incoming_index_maps_targets_to_sources():
    db = DDL_Dict(name="d", schemas=[schema_dict(name="dairy", tables=[
        table_dict(name="institutions", columns=[column_dict(name="institutionid", type="text")]),
        table_dict(name="instruments", columns=[column_dict(name="supplierid", type="text")],
            constraints=[constraint_dict(name="fk", type="REFERENCES", columns=["supplierid"],
                references=reference_dict(schema="dairy", table="institutions", columns=["institutionid"]))]),
    ])])
    idx = build_incoming_index(db)
    entry = idx[("dairy", "institutions")][0]
    assert entry["schema"] == "dairy" and entry["table"] == "instruments"
    assert entry["columns"] == ["supplierid"]
    assert entry["target_columns"] == ["institutionid"]
    assert ("dairy", "instruments") not in idx


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def test_column_print_renders_all_columns():
    cols = [
        column_dict(name="cadid", type="text", comment="id"),
        column_dict(name="gender", type="nchar(1)", comment="g"),
    ]
    out = columnPrint(cols)
    assert "*cadid*" in out
    assert "*gender*" in out
    assert "text" in out
    assert "nchar(1)" in out


def test_constraint_print_empty():
    assert constraintPrint([]) == "This table has no constraints"


def test_index_print_empty():
    assert indexPrint([]) == "This table has no index"


def test_constraint_print_renders_ddl():
    rendered = constraintPrint([
        constraint_dict(name="pk", type="PRIMARY KEY", ddl="PRIMARY KEY (cadid)",
                        comment="c", columns=["cadid"])
    ], schema_name="dairy")
    assert "PRIMARY KEY (cadid)" in rendered


def test_constraint_print_links_foreign_key():
    out = constraintPrint([
        constraint_dict(name="fk", type="REFERENCES", ddl="FOREIGN KEY (supplierid) ...",
            columns=["supplierid"],
            references=reference_dict(schema="dairy", table="institutions", columns=["institutionid"]))
    ], schema_name="dairy")
    assert "[institutions](institutions.md)" in out
    assert "institutionid" in out


def test_constraint_print_no_reference_for_primary_key():
    out = constraintPrint([
        constraint_dict(name="pk", type="PRIMARY KEY", ddl="PRIMARY KEY (cadid)", columns=["cadid"])
    ], schema_name="dairy")
    assert "PRIMARY KEY (cadid)" in out


def test_index_print_renders_ddl():
    rendered = indexPrint([
        index_dict(name="cadid_idx", type="btree",
                   ddl="CREATE INDEX cadid_idx ON cows (cadid)", columns=["cadid"])
    ])
    assert "CREATE INDEX cadid_idx ON cows (cadid)" in rendered


# --------------------------------------------------------------------------- #
# Page writers
# --------------------------------------------------------------------------- #
def _sample_table():
    return table_dict(
        name="cows",
        comment="cow table",
        columns=[column_dict(name="cadid", type="text", comment="id")],
        constraints=[
            constraint_dict(name="pk", type="PRIMARY KEY", ddl="PRIMARY KEY (cadid)",
                            comment="c", columns=["cadid"])
        ],
    )


def test_table_page_writes_markdown(tmp_path):
    table_page(_sample_table(), tmp_path / "tables", "dairy", [])
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
    table = table_dict(name="bare", comment="x",
                       columns=[column_dict(name="c", type="text", comment="")])
    table_page(table, tmp_path / "tables", "dairy", [])
    text = (tmp_path / "tables" / "bare.md").read_text()
    assert "This table has no constraints" in text
    assert "This table has no index" in text


def test_table_page_lists_references(tmp_path):
    table = table_dict(name="instruments",
        columns=[column_dict(name="supplierid", type="text")],
        constraints=[constraint_dict(name="fk", type="REFERENCES", ddl="FK ...",
            columns=["supplierid"],
            references=reference_dict(schema="dairy", table="institutions", columns=["institutionid"]))])
    table_page(table, tmp_path / "tables", "dairy", [])
    text = (tmp_path / "tables" / "instruments.md").read_text()
    assert "**References**" in text
    assert "[institutions](institutions.md)" in text
    assert "**Referenced By**" in text


def test_table_page_lists_referenced_by(tmp_path):
    table = table_dict(name="institutions", columns=[column_dict(name="institutionid", type="text")])
    incoming = [{"schema": "dairy", "table": "instruments",
                 "columns": ["supplierid"], "target_columns": ["institutionid"]}]
    table_page(table, tmp_path / "tables", "dairy", incoming)
    text = (tmp_path / "tables" / "institutions.md").read_text()
    assert "[instruments](instruments.md)" in text


def test_schema_page_writes_schema_and_tables(tmp_path):
    schema = schema_dict(name="dairy", comment="the dairy schema", tables=[_sample_table()])
    schema_page(schema, tmp_path / "dairy", {})
    schema_md = tmp_path / "dairy" / "index.md"
    assert schema_md.is_file()
    text = schema_md.read_text()
    assert "`dairy` Schema" in text
    assert "[cows](tables/cows.md)" in text
    assert (tmp_path / "dairy" / "tables" / "cows.md").is_file()


def test_database_page_writes_index_and_schemas(tmp_path):
    database = DDL_Dict(
        name="dairymodel", comment="the whole db",
        schemas=[schema_dict(name="dairy", comment="dairy schema", tables=[_sample_table()])],
    )
    database_page(database, tmp_path / "database")
    index = tmp_path / "database" / "index.md"
    assert index.is_file()
    text = index.read_text()
    assert "# dairymodel" in text
    assert "[dairy](./dairy/index.md)" in text
    assert (tmp_path / "database" / "dairy" / "index.md").is_file()


def test_document_database_respects_path(tmp_path):
    """document_database writes under the path it is given (no hardcoded 'docs/')."""
    database = DDL_Dict(
        name="dairymodel", comment="db",
        schemas=[schema_dict(name="dairy", comment="s", tables=[_sample_table()])],
    )
    document_database(database, tmp_path / "out")
    assert (tmp_path / "out" / "database" / "index.md").is_file()
