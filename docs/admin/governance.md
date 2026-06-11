# Data Governance

The files in this repository represent the structure and relationships between data objects at the Dairy Education and Research Centre. As much as possible they should represent accepted relationships and data models for objects in the literature or as proposed by standards groups. For example, the definition and fields used to describe an `instrument` at DERC borrow from [Stocker et al (2020)](https://datascience.codata.org/articles/1135/files/submission/proof/1135-1-7520-2-10-20200506.pdf).

The data model is currently defined informally in an organic manner:

<div class="grid cards" markdown>

-   :material-pencil-ruler:{ .lg .middle } __Implementation__

    ---

    * Simon Goring

-   :material-database-check:{ .lg .middle } __Expert Review__
  
    ---

    * Marina von Keyserlingk
    * Dan Weary
    * Leluo Guan
    * Ronaldo Cerri

</div>

## File Structure

With this governance model in mind, we develop a set of YAML files to represent various entities and their relationships. The goal is to enable us to look at difference elements of the data model independently, and to use model validation to bring them all together.

All raw YAML files are available in the [data_definitions](https://github.com/UBC-DERC/data_model/tree/main/data_definitions) folder and accompanying subfolders.

An early version of this project was structured in this way, where individual `yaml` files represent specific definitions for the database, the schema, tables and columns used to define the data objects.

```
./data_definitions
├── dairymodel.yaml
├── schemas
│   ├── apps.yaml
│   ├── dairy.yaml
│   ├── apptables [empty]
│   └── dairytables
│       ├── columns
│       │   ├── datasetid.yaml
.       .   .   ...
│       │   └── instrumentid.yaml
│       ├── cows.yaml
│       ├── datasetidentifiers.yml
.       .   ...
│       └── instruments.yaml
└── users
    └── users.yaml
```

This data structure allows us to directly identify and modify particular elements of the data model in a relatively human-readable way, and to validate the overall model as it matures.

## Model Review

As the data model matures, each round of data model review (as opposed to code development) will be accompanied by GitHub Issues, a Pull Request and a Release, to provide a clear model of accountability for decisions made.

Until the release of v0.1 of the Dairy Data Model, we will use the more common practice of [GitFlow-style](https://www.gitkraken.com/learn/git/git-flow) commits.

## Contribution Guidelines

We have a [Contributors Guide](https://github.com/UBC-DERC/data_model/blob/main/CONTRIBUTING.md) that is still in development, to identify the process for explicitly contributing to the data model. Modifications will identify the field or table to be modified, identify changes to be made, and explain why the change needs to be made.
