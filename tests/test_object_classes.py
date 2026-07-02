"""Tests for the pydantic models in data_model.object_classes.

Covers reference_dict (the foreign target of a constraint), and constraint_dict
which separates a constraint's own/local columns from an optional foreign
target that only FOREIGN KEY constraints may carry.
"""
import pytest
from pydantic import ValidationError

from data_model.object_classes import (
    reference_dict, constraint_dict, index_dict, table_dict, column_dict,
    DDL_Dict, schema_dict,
)


def test_table_accepts_schema_key_and_forbids_unknown():
    t = table_dict(name="cows", schema="dairy", columns=[column_dict(name="id", type="text")])
    assert t.schema_ == "dairy"
    with pytest.raises(ValidationError):
        table_dict(name="cows", columns=[column_dict(name="id", type="text")], bogus=1)


def test_column_forbids_unknown_keys():
    with pytest.raises(ValidationError):
        column_dict(name="id", type="text", bogus=1)


def test_database_accepts_owner_and_forbids_unknown():
    db = DDL_Dict(name="d", owner="postgres",
                  schemas=[schema_dict(name="dairy", tables=[table_dict(
                      name="cows", columns=[column_dict(name="id", type="text")])])])
    assert db.owner == "postgres"
    with pytest.raises(ValidationError):
        DDL_Dict(name="d", schemas=[], nonsense=1)


def test_reference_defaults_schema_and_table_to_none():
    ref = reference_dict(columns=["cadid"])
    assert ref.schema_ is None
    assert ref.table is None
    assert ref.columns == ["cadid"]


def test_reference_accepts_schema_and_table_from_yaml():
    ref = reference_dict(**{"schema": "dairy", "table": "cows", "columns": ["cadid"]})
    assert ref.schema_ == "dairy"
    assert ref.table == "cows"


def test_reference_requires_columns():
    with pytest.raises(ValidationError):
        reference_dict(schema="dairy", table="cows")


def test_reference_forbids_unknown_keys():
    with pytest.raises(ValidationError):
        reference_dict(table="cows", columns=["cadid"], referencedTable="cows")


def test_foreign_key_accepts_references():
    c = constraint_dict(
        name="fk", type="FOREIGN KEY", columns=["supplierid"],
        references=reference_dict(table="institutions", columns=["institutionid"]),
    )
    assert c.references.table == "institutions"


def test_primary_key_rejects_references():
    with pytest.raises(ValidationError):
        constraint_dict(
            name="pk", type="PRIMARY KEY", columns=["id"],
            references=reference_dict(table="cows", columns=["id"]),
        )


def test_check_keeps_local_columns_and_no_references():
    c = constraint_dict(name="chk", type="CHECK", ddl="CHECK (x > 0)", columns=["x"])
    assert c.columns == ["x"]
    assert c.references is None


def test_constraint_forbids_unknown_keys():
    with pytest.raises(ValidationError):
        constraint_dict(name="c", type="PRIMARY KEY", referencedTable="cows")


def test_index_has_local_columns_and_no_reference():
    idx = index_dict(name="i", ddl="CREATE INDEX ...", columns=["a", "b"])
    assert idx.columns == ["a", "b"]
    with pytest.raises(ValidationError):
        index_dict(name="i", ddl="...", reference=[{"table": "cows", "columns": ["a"]}])
