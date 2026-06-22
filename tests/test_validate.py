"""Tests for data_model.validate.validate_object.

validate_object checks that an object contains no keys beyond those declared
in validation.yaml for its type, and merges any ``ref:`` target into the
object. These tests cover both behaviours plus the documented gaps.
"""
import pytest

from data_model import validate_object


@pytest.fixture
def schema():
    """A minimal validation schema standing in for validation.yaml."""
    return {
        "table": {"keys": ["name", "type", "schema", "columns", "comment"]},
        "column": {"keys": ["name", "type", "comment"]},
    }


def test_clean_object_passes_unchanged(schema):
    obj = {"name": "cows", "type": "BASE TABLE", "schema": "dairy"}
    result = validate_object(schema, dict(obj), ddl_type="table")
    assert result == obj


def test_extra_key_raises_assertion(schema):
    obj = {"name": "cows", "bogus": 1}
    with pytest.raises(AssertionError) as exc:
        validate_object(schema, obj, ddl_type="table")
    assert "bogus" in str(exc.value)


def test_ref_is_an_allowed_key(schema):
    """'ref' is implicitly allowed for every type."""
    # Only legal because validate_object appends 'ref' to the allowed keys.
    obj = {"name": "datecreated", "type": "datetime"}
    result = validate_object(schema, obj, ddl_type="column")
    assert result["name"] == "datecreated"


def test_ref_target_is_merged(schema, write_yaml):
    target = write_yaml("col.yaml", [{"name": "datecreated", "type": "datetime"}])
    obj = {"ref": str(target), "comment": "local override comment"}

    result = validate_object(schema, obj, ddl_type="column")

    # Keys from both the ref target and the local object are present.
    assert result["name"] == "datecreated"
    assert result["type"] == "datetime"
    assert result["comment"] == "local override comment"


def test_missing_required_keys_are_not_caught(schema):
    """Documents a gap: validate_object never checks for *missing* keys.

    An empty table definition passes validation today. Update this test
    if required-field validation is added.
    """
    result = validate_object(schema, {}, ddl_type="table")
    assert result == {}
