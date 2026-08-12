"""Shared pytest fixtures for the data_model test suite."""
from pathlib import Path

import pytest
import yaml

# Directory holding small, hand-written YAML fixtures for unit tests.
FIXTURES = Path(__file__).parent / "samples"

# Repository root and the real definition files, used for integration tests.
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DEFINITIONS = REPO_ROOT / "examples/data_definitions"


@pytest.fixture
def fixtures_dir():
    """Path to the tests/fixtures directory."""
    return FIXTURES


@pytest.fixture
def write_yaml(tmp_path):
    """Factory that writes a Python object to a YAML file in tmp_path.

    Usage:
        path = write_yaml("thing.yaml", [{"name": "x"}])
    """

    def _write(name, obj):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as handle:
            yaml.safe_dump(obj, handle)
        return path

    return _write
