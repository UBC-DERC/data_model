"""Tests for the data-model command-line entry point."""
import yaml

from data_model.cli import main




def test_cli_success_writes_both_artifacts(tmp_path):
    out = tmp_path / "output.yaml"
    docs = tmp_path / "docs"
    code = main([
        "examples/data_definitions/dairymodel.yaml",
        "--docs", str(docs),
        "--output", str(out),
    ])
    assert code == 0
    assert out.exists()
    assert yaml.safe_load(out.read_text())["name"] == "dairymodel"
    assert docs.exists() and any(docs.iterdir())


def test_cli_invalid_entry_exits_1_and_writes_nothing(tmp_path, write_yaml, capsys):
    # A table with a FK to a non-existent table -> ReferenceCheckError.
    write_yaml("tables/t1.yaml", [{
        "name": "t1",
        "columns": [{"name": "id", "type": "text"}],
        "constraints": [{
            "name": "ghost_fk", "type": "REFERENCES", "columns": ["id"],
            "references": {"table": "ghost", "columns": ["id"]},
        }],
    }])
    tables_dir = tmp_path / "tables"
    schema = write_yaml("schema.yaml", [{"name": "dairy", "tables": [{"ref": str(tables_dir)}]}])
    entry = write_yaml("db.yaml", [{"name": "d", "schemas": [{"ref": str(schema)}]}])

    out = tmp_path / "output.yaml"
    code = main([str(entry), "--docs", str(tmp_path / "docs"), "--output", str(out)])

    assert code == 1
    assert not out.exists()
    err = capsys.readouterr().err
    assert "ghost" in err
