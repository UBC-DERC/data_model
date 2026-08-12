# tests/test_output_yaml.py
import os
import subprocess
from pathlib import Path
import yaml

EXAMPLE = Path("examples/data_definitions/dairymodel.yaml")
GOLDEN = Path("tests/golden/output.yaml")

def test_output_yaml_matches_golden(tmp_path):
    output = tmp_path / "output.yaml"
    subprocess.run(
        ["data-model", str(EXAMPLE),
         "--output", str(output)],
        check=True,
    )

    produced = yaml.safe_load(output.read_text())

    if os.environ.get("UPDATE_GOLDEN"):
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(yaml.safe_dump(produced, sort_keys=True))

    expected = yaml.safe_load(GOLDEN.read_text())
    assert produced == expected