"""Tests for data_model.model_build.build_tables.

build_tables turns validated table dicts into table_dict models, but converts
pydantic's numeric-path ValidationErrors into readable messages that name the
offending table and constraint, and reports every bad table at once.
"""
import pytest

from data_model.model_build import ModelValidationError, build_tables
from data_model.object_classes import table_dict

GOOD_TABLE = {
    "name": "cows",
    "columns": [{"name": "cadid", "type": "text"}],
    "constraints": [{"name": "pk", "type": "PRIMARY KEY", "columns": ["cadid"]}],
}


def test_valid_tables_build_into_models():
    result = build_tables([GOOD_TABLE])
    assert len(result) == 1
    assert isinstance(result[0], table_dict)
    assert result[0].name == "cows"


def test_extra_key_names_table_and_constraint():
    bad = {
        "name": "instruments",
        "columns": [{"name": "supplierid", "type": "text"}],
        "constraints": [
            {"name": "supplier_fkey", "type": "REFERENCES", "referencedTable": "institutions"}
        ],
    }
    with pytest.raises(ModelValidationError) as exc:
        build_tables([bad])
    message = str(exc.value)
    assert "instruments" in message
    assert "supplier_fkey" in message
    assert "referencedTable" in message


def test_references_on_primary_key_is_reported_clearly():
    bad = {
        "name": "cows",
        "columns": [{"name": "cadid", "type": "text"}],
        "constraints": [
            {"name": "cowpk", "type": "PRIMARY KEY", "columns": ["cadid"],
             "references": {"table": "cows", "columns": ["cadid"]}}
        ],
    }
    with pytest.raises(ModelValidationError) as exc:
        build_tables([bad])
    message = str(exc.value)
    assert "cowpk" in message
    assert "REFERENCES" in message


def test_all_bad_tables_reported_together():
    bad_a = {
        "name": "a", "columns": [{"name": "id", "type": "text"}],
        "constraints": [{"name": "a_c", "type": "PRIMARY KEY", "bogus": 1}],
    }
    bad_b = {
        "name": "b", "columns": [{"name": "id", "type": "text"}],
        "constraints": [{"name": "b_c", "type": "PRIMARY KEY", "junk": 1}],
    }
    with pytest.raises(ModelValidationError) as exc:
        build_tables([bad_a, bad_b])
    message = str(exc.value)
    assert "a_c" in message and "b_c" in message
