# API Reference

This section documents the `data_model` Python package, generated directly from
the source docstrings. The package implements a **load → validate → render**
pipeline that reads the YAML definition ofa database (see the example in `examples/data_definitions/`), validates them
structurally (using Pydantic models) and validates constraint reference to produce a single YAML object representing the database, its indices, tables, constraints and columns. The `data_model` also serves to render
Markdown documentation for the generated database, including cross-references.

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
| [`cli`](cli.md) | The command line interface for the project. |
| [`object_classes`](object_classes.md) | The component Pydantic classes defining objects within the database. |
| [`load_files`](load_files.md) | Read a YAML file (or directory) into a dict/list |
| [`load_database`](load_database.md) | Load the database root and resolve schema refs |
| [`load_schema`](load_schema.md) | Load a schema and resolve table refs |
| [`load_tables`](load_tables.md) | Load tables and resolve column refs |
| [`load_columns`](load_columns.md) | Load and validate a column fragment |
| [`model_build`](model_build.md) | The tooling to build the full data model from composite components. |
| [`create_docs`](create_docs.md) | Render the model as Markdown documentation |
