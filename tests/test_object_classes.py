"""Tests for the pydantic models in data_model.object_classes.

Focused on reference_dict, which identifies the table (and, now, the schema)
that a constraint or index points at. A reference must name a schema so that
cross-schema references can be resolved and validated.
"""
import pytest
from pydantic import ValidationError

from data_model.object_classes import reference_dict


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
