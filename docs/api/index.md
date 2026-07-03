# API Reference

This section documents the `data_model` Python package, generated directly from
the source docstrings. The package implements a **load → validate → render**
pipeline that reads the YAML definitions in `data_definitions/`, validates them
structurally (via the pydantic models) and by cross-reference, and renders
Markdown documentation.

## Public API

The following objects are exported from the top-level `data_model` package:

::: data_model
    options:
      show_source: false
      members:
        - load_file
        - load_database
        - load_schema
        - load_tables
        - document_database

## Modules

| Module | Responsibility |
|--------|----------------|
| [`load_files`](load_files.md) | Read a YAML file (or directory) into a dict/list |
| [`load_database`](load_database.md) | Load the database root and resolve schema refs |
| [`load_schema`](load_schema.md) | Load a schema and resolve table refs |
| [`load_tables`](load_tables.md) | Load tables and resolve column refs |
| [`load_columns`](load_columns.md) | Load and validate a column fragment |
| [`createDocs`](createDocs.md) | Render the model as Markdown documentation |
