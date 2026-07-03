# The DERC Database Model

A fully open data model based on best practices across industries and academic fields. This database is intended to support the research activities across the UBC [Dairy Education and Research Center](https://dairycentre.landfood.ubc.ca/) in Agassiz, British Columbia.

## Contents


<div class="grid cards" markdown>

-   :material-clipboard-list:{ .lg .middle } __[Executive Summary](summary/executive_summary.md)__

    ---

    Project overview, outcomes and success metrics.

-   :material-sitemap:{ .lg .middle } __[Governance and Guidance](admin/governance.md)__
  
    ---

    How this project is governed and managed from a personel perspective.

-   :material-lightbulb:{ .lg .middle } __[Resources and Concepts](resources.md)__

    ---

    Tools for project management, and database-related concepts to support efficient management.

-   :material-database-check:{ .lg .middle } __[Table Structure](database/index.md)__

    ---

    Documentation of the database itself, including table overviews, definitions and links.

</div>


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
