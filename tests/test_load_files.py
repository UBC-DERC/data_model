"""Tests for data_model.load_files.load_file.

load_file is the foundation of the whole loading pipeline, so these tests
pin down its dispatch behaviour and document two known fragilities:

  * it only returns the *first* element of a YAML list (``[0]``);
  * directory loading globs ``*.yaml`` only, silently ignoring ``*.yml``.
"""
import pytest

from data_model import load_file


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


def test_load_directory_ignores_yml_extension(write_yaml):
    """Known bug: ``.yml`` files are silently skipped by glob('*.yaml').

    The real repo contains ``datasetidentifiers.yml`` which is therefore
    never loaded. This test documents the bug; flip the assertion once
    load_file is fixed to accept both extensions.
    """
    write_yaml("mixed/keep.yaml", [{"name": "keep"}])
    directory = (write_yaml("mixed/dropped.yml", [{"name": "dropped"}])).parent

    result = load_file(str(directory))
    names = [item["name"] for item in result]

    assert "keep" in names
    assert "dropped" not in names  # <-- ideally this should be present


def test_load_missing_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_file(str(tmp_path / "does_not_exist.yaml"))
