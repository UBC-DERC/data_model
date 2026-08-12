"""Tests for data_model.load_files.load_file.

load_file is the foundation of the whole loading pipeline, so these tests
pin down its dispatch behaviour and document two known fragilities:

  * it only returns the *first* element of a YAML list (``[0]``);
  * directory loading globs ``*.yaml`` only, silently ignoring ``*.yml``.
"""
import pytest

import data_model as dm
from data_model import load_file
from data_model.load_files import resolve_ref


def test_resolve_ref_merges_target(write_yaml):
    target = write_yaml("col.yaml", [{"name": "datecreated", "type": "datetime"}])
    result = resolve_ref({"ref": str(target), "comment": "local"})
    assert result["name"] == "datecreated"
    assert result["type"] == "datetime"
    assert result["comment"] == "local"


def test_resolve_ref_passes_through_without_ref():
    obj = {"name": "cows", "type": "text"}
    assert resolve_ref(dict(obj)) == obj


def test_resolve_ref_resolves_relative_to_base_dir(write_yaml):
    """A relative ref is resolved against base_dir, not the cwd."""
    target = write_yaml("nested/col.yaml", [{"name": "c", "type": "text"}])
    result = resolve_ref({"ref": "col.yaml"}, base_dir=target.parent)
    assert result["name"] == "c"


def test_load_database_resolves_refs_relative_to_entry_file(write_yaml, monkeypatch, tmp_path):
    """Refs resolve relative to the file that contains them, regardless of cwd.

    The entry file references ``schemas/s.yaml``; that schema references a
    table dir ``tables``; the table references ``columns/id.yaml`` -- all
    written relative to their own directory. Loading works even when the
    process runs from an unrelated working directory.
    """
    write_yaml("proj/schemas/s.yaml", [{"name": "dairy", "tables": [{"ref": "tables"}]}])
    # The table file lives in the tables dir and points at columns relative to it.
    write_yaml("proj/schemas/tables/cows.yaml", [{
        "name": "cows",
        "columns": [{"ref": "columns/name.yaml"}],
    }])
    write_yaml("proj/schemas/tables/columns/name.yaml", [{"name": "name", "type": "text"}])
    entry = write_yaml("proj/db.yaml", [{"name": "d", "schemas": [{"ref": "schemas/s.yaml"}]}])

    # Run from an unrelated directory to prove cwd-independence.
    foreign = tmp_path / "elsewhere"
    foreign.mkdir()
    monkeypatch.chdir(foreign)

    db = dm.load_database(str(entry))
    assert [s.name for s in db.schemas] == ["dairy"]
    cows = db.schemas[0].tables[0]
    assert cows.name == "cows"
    assert {c.name for c in cows.columns} == {"name"}


def test_load_single_file_returns_first_element(write_yaml):
    path = write_yaml("single.yaml", [{"name": "alpha"}])
    result = load_file(str(path))
    assert result == {"name": "alpha"}


def test_load_file_only_returns_first_list_element(write_yaml):
    """load_file uses ``safe_load(file)[0]`` and drops the rest.

    This documents current behaviour. If multi-document files should be
    supported, this test should be updated and load_file fixed.
    """
    path = write_yaml("multi.yaml", [{"name": "first"}, {"name": "second"}])
    result = load_file(str(path))
    assert result == {"name": "first"}


def test_load_directory_returns_list_of_files(write_yaml):
    write_yaml("dir/a.yaml", [{"name": "a"}])
    write_yaml("dir/b.yaml", [{"name": "b"}])
    directory = (write_yaml("dir/c.yaml", [{"name": "c"}])).parent

    result = load_file(str(directory))
    assert isinstance(result, list)
    names = sorted(item["name"] for item in result)
    assert names == ["a", "b", "c"]


def test_load_directory_accepts_both_extensions(write_yaml):
    """Both ``.yaml`` and ``.yml`` files are loaded from a directory.

    Editors disagree on the extension, so the loader must accept either.
    """
    write_yaml("mixed/keep.yaml", [{"name": "keep"}])
    directory = (write_yaml("mixed/dropped.yml", [{"name": "dropped"}])).parent

    result = load_file(str(directory))
    names = [item["name"] for item in result]

    assert "keep" in names
    assert "dropped" in names


def test_load_missing_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_file(str(tmp_path / "does_not_exist.yaml"))
