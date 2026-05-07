# data_model

This project is intended as a repository for the ultimate data model for the DERC Dairy Database: D^3. The model is designed to represent and provide documentation for data elements within the DERC Research data system. Primarily this database is intended to store data to be used for research projects. 

This repository is for `yaml` data representations of the actual data model.  The `yaml` formatting follows the example used by [`tabls`](https://github.com/k1Low/tbls) elsewhere, with an added directory structuring to make individual tables easier to process, modify, validate and document.

## Repository Structure

### data_model

```bash
|- dairymodel.yaml
|\- users
  |- users.yaml
|\- tables
  |\-  cows.yaml
    |- datasets.yaml
    |- ...
```

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
    type: PRIMARY KEY
    def: PRIMARY KEY (columnname, columnname)
    table: cows
    referencedTable:
    - tablename
    columns:
    - columnname
    - columnname
  indexes:
  - name: indexname
    referencedTable:
    - tablename
    columns:
    - columnname
    type: A valid postgres index type.
```

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

<!--
A short description of how this repository is expected to be used.
-->

## Funding Statement

This project was developed with funding from [Farm Credit Canada](https://www.fcc-fac.ca/).