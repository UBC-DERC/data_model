# tests/test_output_yaml.py
from pathlib import Path
import yaml

GOLDEN = Path("tests/samples/output.yaml")

def test_zero_key():
    with open(GOLDEN, 'r') as f:
        file_good = yaml.safe_load(f)
    assert isinstance(file_good,dict), "The file produced isn't a proper dict."