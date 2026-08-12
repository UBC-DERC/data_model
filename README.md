# Human Readable Data Models for Dairy Database

This project is intended as a repository for the ultimate data model for the DERC Dairy Database: D^3. The model is designed to represent and provide documentation for data elements within the DERC Research data system. Primarily this database is intended to store data to be used for research projects.

This repository is for `yaml` data representations of the actual data model.  The `yaml` formatting follows the example used by [`tabls`](https://github.com/k1Low/tbls) elsewhere, with an added directory structuring to make individual tables easier to process, modify, validate and document.

```mermaid
User Consultation --> Data Model
Data Model --> Validation 
Data Model --> Database DDL
```

## Editing/Modifying or Working with the Data Model

We are using version control as our primary method for managing the data model. This (in principle) allows us to create release notes for the model, have discussions and raise issues. Our goal is to manage the model in an inclusive manner that reflects changing user needs, expert knowledge and technical requirements.

Modifications should occur in branches of this repository, they should compile properly with the tools provided, and should contain sufficient annotations that users can understand why these changes have happened and how they support ongoing research.

TODO: Create a "contribution guide".

## Repository Structure

### File and Folder Structure

Within this repository we will create a named folder, here `dairymodel`. Within the folder we will include a set of `yaml` files. These files will contain the critical information for database, schema, table and column definitions. We create these files to support the work of experts in defining the critical fields and concepts used in the database.

The database itself is defined by a folder structure, modeled after PostgreSQL database structure: `database` -> `schema` -> `table` -> `column`. Within each folder, we have individually named files for each of the elements within that hierarchy. Individual files can stand alone, or we can use the `#ref` tag to point to other files. For example, for the database definition we can create a `yaml` file with the text:

```yaml
- name: dairymodel
  schemas:
    - name: dairy
      comment: |
        The main dairy schema, with all data structures used for the farm.
    - name: apps
      comment: |
        The schema used for application specific tables, views and materialized views.
```

or we can use references to sub-folders with the `ref` tag, to point to folder content:

```yaml
- name: dairymodel
  schemas:
    - ref: schemas/dairy.yaml
    - ref: schemas/apps.yaml  
```

Using the `ref` tag also allows us to re-use certain content, for example, columns for understanding data creation dates and data modification dated.

### Dairy Model

The `dairymodel.yaml` file defines the main database-level elements required for the D^3 database. This includes pointers to particular configuration settings (page size, etc), database extensions, schema definitions, and other elements that are required to define the database itself. Some of this configuration may also be defined in the database Dockerfile which is defined elsewhere.

The `users` folder defines user roles for the database, using a "least-privileges" model of inheritence. We aim to limit data privileges as much as possible. This is defined and explained within the `users` yaml file.

The `tables` folder contains definitions of each of the tables created for the database. These follow the `yaml` model:

```yaml
- name: tablename
  type: one of [BASE TABLE, VIEW, MATERIALIZED VIEW]
  schema: one of the schemas defined in the `dairymodel.yaml`
  columns:
  - name: columnname
    type: a valid postgres data type (https://www.postgresql.org/docs/current/datatype.html)
    comment: a text comment (may include html or markdown)
  constraints:
  - name: constraintname
    comment: |
        Some example primary key.
    type: one of [PRIMARY KEY, REFERENCES, UNIQUE, CHECK]
    ddl: PRIMARY KEY (columnname, columnname)   # authoritative SQL for this constraint
    columns:                                     # the constraint's OWN (local) columns
    - columnname
    - columnname
  - name: a_foreign_key
    comment: |
        A foreign key also names the table it points at.
    type: REFERENCES
    ddl: FOREIGN KEY (localcolumn) REFERENCES othertable (targetcolumn) ON UPDATE CASCADE
    columns:                                     # local column(s) the FK is defined on
    - localcolumn
    references:                                  # only REFERENCES may carry a `references`
      schema: dairy                              # optional; defaults to the owning table's schema
      table: othertable                          # optional; defaults to the owning table (self-FK)
      columns:                                   # the REFERENCED column(s) in the target table
      - targetcolumn
  indexes:
  - name: indexname
    type: A valid postgres index type.
    ddl: CREATE INDEX indexname ON tablename (columnname)
    columns:                                     # indexes carry only local columns
    - columnname
```

Each constraint's `ddl` string is the authoritative SQL used to build the
database. The structured fields exist to help non-SQL users and to let the
tool validate references: a constraint's `columns` must exist in its own table,
and a `references` block (allowed only on `REFERENCES`) must point at an
existing `(schema, table)` whose `columns` exist. When `schema`/`table` are
omitted from a `references` block they default to the owning table.

From these sets of yaml files we can build both documentation using `mkdocs` (in this repository) and we can build the actual SQL DDL for the database (using a Docker image and a separate python package). This structure allows us to clearly document the development of the database, and all its various components.

## Contribution

This project was developed by:

* [![]](https://orcid.org/0000-0002-2700-4605): Simon Goring

Contributions to this repository are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Installing this Package

To install  from this GitHub repository, either install using a graphical tool such as GitKraken or GitHub Desktop, or install from the console using:

```bash
git clone UBC-DERC/data_model.git
cd 
python -m pip install .
```

## How to Use this Repository

Once installed, the `data-model` command validates a model and writes both the
composite YAML artifact and the MkDocs documentation:

```bash
data-model <path/to/entry.yaml> --docs <docs-output-dir> --output <composite.yaml>
```

For the example model bundled in this repository:

```bash
data-model data_definitions/dairymodel.yaml --docs docs --output output.yaml
```

The `data_definitions/` folder is **example input** — point the tool at the
entry file of any directory of definitions.

The command validates before writing anything. Validation runs in two phases:
structural checks on each definition (unknown keys, malformed constraints), and
cross-reference checks across the assembled model (every referenced table and
column must exist). If either phase fails, the command prints **all** problems
at once to stderr, writes **no** output, and exits with a non-zero status —
suitable for gating a deployment pipeline before DDL generation.

The composite `--output` YAML is the fully-resolved model (all `ref:` targets
merged, reference schemas/tables filled in) intended for the downstream DDL
generation stage.

## Funding Statement

This project was developed with funding from [Farm Credit Canada](https://www.fcc-fac.ca/).
