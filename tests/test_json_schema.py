import json

from data_model.json_schema import SCHEMA_URL, build_schema, write_schema
from data_model.object_classes import ddaml_dict


def test_schema_has_dialect_and_id():
    schema = build_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == SCHEMA_URL


def test_schema_matches_root_model():
    schema = build_schema()
    assert schema["title"] == "ddaml_dict"
    assert set(schema["required"]) == {"ddaml_version", "database", "info"}
    assert schema["properties"] == ddaml_dict.model_json_schema()["properties"]


def test_write_schema_round_trips(tmp_path):
    path = write_schema(tmp_path / "nested" / "schema.json")
    assert json.loads(path.read_text()) == build_schema()
