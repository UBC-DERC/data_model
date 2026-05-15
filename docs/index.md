# The DERC Database Model

A fully open data model based on best practices across industries and academic fields. This database is intended to support the research activities across the UBC Dairy Education and Research Center in Agassiz, British Columbia.

## Contents

* [Governance and Guidance](admin/governance.md)
* [Resources and Concepts]()
* [Table Structure]()

## Project layout

```bash
    main.py    # The main production script to turn the 
               # various YAML files into code.
    src/
        data_model/  # The folder for the `data_model` python package.
    docs/            # Documentation pages.
    assets/          # Images and supporting data for documentation and testing.
    tests/           # PyTest testing modules
    data_definition/ # Folder with composite YAML files for database definitions.
    validation.yaml  # Supporting file to define valid fields for db elements.
    pyproject.toml   # Package infrastructure.
    mkdocs.yaml      # Documentation metadata.
```
