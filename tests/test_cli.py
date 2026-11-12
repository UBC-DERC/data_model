"""Tests for the data-model command-line entry point."""

import pytest
import yaml

from ddlml.cli import main


def test_cli_success_writes_both_artifacts(tmp_path):
    """

    Args:
        tmp_path (_type_): _description_
    We're testing to make sure that the CLI writes both the validated
    YAML file (to whatever temp folder we're using) and the mkdocs
    documentaion.
    """
    out = tmp_path / "output.yaml"
    docs = tmp_path / "docs"
    code = main(
        [
            "examples/data_definitions/dairymodel.yaml",
            "--docs",
            str(docs),
            "--output",
            str(out),
        ]
    )
    assert code == 0
    assert out.exists()
    assert yaml.safe_load(out.read_text())["database"]["name"] == "dairymodel"
    assert docs.exists() and any(docs.iterdir())
    #assert yaml.safe_load(out.read_text())["database"]["schemas"][0]["x-example"] == "example"


def test_cli_invalid_entry_exits_1_and_writes_nothing(tmp_path, write_yaml, capsys):
    # A table with a FK to a non-existent table -> ReferenceCheckError.
    write_yaml(
        "tables/t1.yaml",
        [
            {
                "name": "t1",
                "columns": [{"name": "id", "type": "text"}],
                "constraints": [
                    {
                        "name": "ghost_fk",
                        "type": "REFERENCES",
                        "columns": ["id"],
                        "references": {"table": "ghost", "columns": ["id"]},
                    }
                ],
            }
        ],
    )
    tables_dir = tmp_path / "tables"
    schema = write_yaml(
        "schema.yaml", [{"name": "dairy", "tables": [{"$ref": str(tables_dir)}]}]
    )
    entry = write_yaml(
        "db.yaml", [{"database": {"name": "d", "schemas": [{"$ref": str(schema)}]}}]
    )

    out = tmp_path / "output.yaml"
    code = main([str(entry), "--docs", str(tmp_path / "docs"), "--output", str(out)])

    assert code == 1
    assert not out.exists()
    err = capsys.readouterr().err
    assert "ghost" in err


def test_ddlml_with_no_database_exits_1_and_writes_nothing(
    tmp_path, write_yaml, capsys
):
    # A database entry file with no 'database:' block -> ModelValidationError.
    entry = write_yaml("db.yaml", [{"bogus": "value"}])

    out = tmp_path / "output.yaml"
    code = main([str(entry), "--docs", str(tmp_path / "docs"), "--output", str(out)])

    assert code == 1
    assert not out.exists()
    err = capsys.readouterr().err
    assert "no 'database:' block" in err


def test_cli_missing_output_exits_2(tmp_path, capsys):
    entry = tmp_path / "db.yaml"
    entry.write_text("database:\n  name: d")

    with pytest.raises(SystemExit) as exc:
        main([str(entry)])

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "the following arguments are required: -o/--output" in err
    assert not any(tmp_path.iterdir()) or list(tmp_path.iterdir()) == [entry]

def test_cli_missing_entry_exits_1_without_traceback(tmp_path, capsys):
    out = tmp_path / "output.yaml"
    code = main([str(tmp_path / "nope.yaml"), "--output", str(out)])

    assert code == 1
    assert not out.exists()
    err = capsys.readouterr().err
    assert "nope.yaml" in err
    assert "Traceback" not in err


def test_cli_missing_ref_target_exits_1(tmp_path, write_yaml, capsys):
    entry = write_yaml(
        "db.yaml",
        [{"database": {"name": "d", "schemas": [{"$ref": "schemas/missing.yaml"}]}}],
    )
    out = tmp_path / "output.yaml"
    code = main([str(entry), "--output", str(out)])

    assert code == 1
    assert not out.exists()
    assert "missing.yaml" in capsys.readouterr().err
