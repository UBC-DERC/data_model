"""Testing the construction of the ddlml object, and the use of the info_dict class"""
import pytest
from pydantic import ValidationError

from ddlml.object_classes import ddlml_dict, CURRENT_DDLML_VERSION


def test_old_version_fails():
  with pytest.raises(ValidationError):
    ddlml_dict(
      ddlml_version="2024.10.4",
      database={
              "name": "test_db",
              "schemas": []
              },
      info={
        "version": "2026.10.4",
        "title": "Test Model",
        "summary": "A test model for testing purposes",
        "contacts": [],
      },
    )

def test_current_version_passes():
    ddlml_dict(
      ddlml_version=CURRENT_DDLML_VERSION,
      database={
        "name": "test_db",
        "schemas": []
        },
      info={
        "version": "2026.10.4",
        "title": "Test Model",
        "summary": "A test model for testing purposes",
        "contacts": [],
      },
    )
