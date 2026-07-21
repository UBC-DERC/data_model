"""Tests for data_model.check_references.

Reference checking runs across the whole assembled model. It first resolves
each foreign target's omitted schema/table from the owning table's context,
then reports *every* problem at the end: local columns that do not exist in the
owning table, and foreign targets whose table or columns do not exist.
"""
import pytest

from data_model.object_classes import (
    DDL_Dict,
    schema_dict,
    table_dict,
    column_dict,
    constraint_dict,
    reference_dict,
)
from data_model.check_crossreferences import (
    find_missing_references,
    check_references,
    resolve_references,
    ReferenceCheckError,
)



def _cols(*names):
    return [column_dict(name=n, type="text") for n in names]


def _table(name, *, columns=("id",), constraints=None):
    return table_dict(
        name=name,
        columns=_cols(*columns),
        constraints=constraints or [],
    )


def _fk(name, references, columns=("id",)):
    return constraint_dict(
        name=name, type="FOREIGN KEY", columns=list(columns), references=references
    )


def _db(*schemas):
    return DDL_Dict(name="dairymodel", schemas=list(schemas))


# --- resolution -----------------------------------------------------------

def test_resolution_defaults_schema_to_owning_schema():
    db = _db(schema_dict(name="dairy", tables=[
        _table("calves", constraints=[_fk("fk", reference_dict(table="cows", columns=["id"]))]),
        _table("cows"),
    ]))
    resolve_references(db)
    ref = db.schemas[0].tables[0].constraints[0].references
    assert ref.schema_ == "dairy"
    assert ref.table == "cows"


def test_resolution_defaults_table_to_owning_table():
    db = _db(schema_dict(name="dairy", tables=[
        _table("cows", constraints=[_fk("selffk", reference_dict(columns=["id"]))]),
    ]))
    resolve_references(db)
    ref = db.schemas[0].tables[0].constraints[0].references
    assert ref.schema_ == "dairy"
    assert ref.table == "cows"


def test_resolution_leaves_explicit_values_untouched():
    db = _db(
        schema_dict(name="dairy", tables=[
            _table("audit", constraints=[_fk("fk", reference_dict(schema="apps", table="logs", columns=["id"]))]),
        ]),
        schema_dict(name="apps", tables=[_table("logs")]),
    )
    resolve_references(db)
    ref = db.schemas[0].tables[0].constraints[0].references
    assert ref.schema_ == "apps" and ref.table == "logs"


# --- foreign target existence ---------------------------------------------

def test_valid_fk_resolves():
    db = _db(schema_dict(name="dairy", tables=[
        _table("cows"),
        _table("calves", constraints=[_fk("fk", reference_dict(table="cows", columns=["id"]))]),
    ]))
    assert find_missing_references(db) == []


def test_missing_table_is_reported():
    db = _db(schema_dict(name="dairy", tables=[
        _table("calves", constraints=[_fk("dam_fk", reference_dict(table="cows", columns=["id"]))]),
    ]))
    problems = find_missing_references(db)
    assert len(problems) == 1
    assert "dairy.cows" in problems[0] and "dam_fk" in problems[0]


def test_wrong_schema_is_reported():
    db = _db(
        schema_dict(name="dairy", tables=[
            _table("calves", constraints=[_fk("dam_fk", reference_dict(schema="apps", table="cows", columns=["id"]))]),
        ]),
        schema_dict(name="apps", tables=[_table("logs")]),
    )
    problems = find_missing_references(db)
    assert len(problems) == 1
    assert "apps.cows" in problems[0]


def test_cross_schema_reference_resolves():
    db = _db(
        schema_dict(name="dairy", tables=[_table("cows")]),
        schema_dict(name="apps", tables=[
            _table("audit", constraints=[_fk("cow_fk", reference_dict(schema="dairy", table="cows", columns=["id"]))]),
        ]),
    )
    assert find_missing_references(db) == []


# --- column existence ------------------------------------------------------

def test_local_column_missing_is_reported():
    db = _db(schema_dict(name="dairy", tables=[
        table_dict(name="cows", columns=_cols("cadid"),
                   constraints=[constraint_dict(name="pk", type="PRIMARY KEY", columns=["ghostcol"])]),
    ]))
    problems = find_missing_references(db)
    assert len(problems) == 1
    assert "ghostcol" in problems[0]


def test_fk_target_column_missing_is_reported():
    db = _db(schema_dict(name="dairy", tables=[
        table_dict(name="institutions", columns=_cols("institutionid")),
        table_dict(name="instruments", columns=_cols("supplierid"),
                   constraints=[_fk("fk", reference_dict(schema="dairy", table="institutions", columns=["ghostid"]),
                                    columns=("supplierid",))]),
    ]))
    problems = find_missing_references(db)
    assert any("ghostid" in p for p in problems)


def test_valid_fk_with_columns_resolves():
    db = _db(schema_dict(name="dairy", tables=[
        table_dict(name="institutions", columns=_cols("institutionid")),
        table_dict(name="instruments", columns=_cols("supplierid"),
                   constraints=[_fk("fk", reference_dict(table="institutions", columns=["institutionid"]),
                                    columns=("supplierid",))]),
    ]))
    assert find_missing_references(db) == []


def test_self_fk_with_defaults_passes():
    db = _db(schema_dict(name="dairy", tables=[
        table_dict(name="cows", columns=_cols("cadid"),
                   constraints=[_fk("damfk", reference_dict(columns=["cadid"]), columns=("cadid",))]),
    ]))
    assert check_references(db) is db


# --- collection / raising --------------------------------------------------

def test_all_failures_collected_not_just_first():
    db = _db(schema_dict(name="dairy", tables=[
        _table("calves", constraints=[
            _fk("a_fk", reference_dict(table="ghost_a", columns=["id"])),
            _fk("b_fk", reference_dict(table="ghost_b", columns=["id"])),
        ]),
    ]))
    problems = find_missing_references(db)
    assert len(problems) == 2
    joined = "\n".join(problems)
    assert "ghost_a" in joined and "ghost_b" in joined


def test_check_references_raises_with_all_problems():
    db = _db(schema_dict(name="dairy", tables=[
        _table("calves", constraints=[
            _fk("a_fk", reference_dict(table="ghost_a", columns=["id"])),
            _fk("b_fk", reference_dict(table="ghost_b", columns=["id"])),
        ]),
    ]))
    with pytest.raises(ReferenceCheckError) as exc:
        check_references(db)
    message = str(exc.value)
    assert "ghost_a" in message and "ghost_b" in message


def test_check_references_returns_db_when_clean():
    db = _db(schema_dict(name="dairy", tables=[_table("cows")]))
    assert check_references(db) is db


def test_real_example_model_loads_and_checks():
    import data_model as dm
    db = dm.load_database("tests/samples/examples/data_definitions/dairymodel.yaml")
    assert [s.name for s in db.schemas] == ["dairy", "apps"]
