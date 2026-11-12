import json

from ddlml.json_schema import SCHEMA_URL, build_schema, write_schema
from ddlml.object_classes import ddlml_dict


def test_schema_has_dialect_and_id():
    schema = build_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == SCHEMA_URL


def test_schema_matches_root_model():
    schema = build_schema()
    assert schema["title"] == "ddlml_dict"
    assert set(schema["required"]) == {"ddlml_version", "database", "info"}
    assert schema["properties"] == ddlml_dict.model_json_schema()["properties"]


def test_write_schema_round_trips(tmp_path):
    path = write_schema(tmp_path / "nested" / "schema.json")
    assert json.loads(path.read_text()) == build_schema()
