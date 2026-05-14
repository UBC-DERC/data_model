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

With this model, we develop a set of YAML files to represent various entities and their relationships. All raw YAML files are available in the [data_definitions](https://github.com/UBC-DERC/data_model/tree/main/data_definitions) folder and accompanying subfolders.

## Model Review

As the data model matures, each round of data model review (as opposed to code development) will be accompanied by GitHub Issues, a Pull Request and a Release, to provide a clear model of accountability for decisions made.

Until the release of v0.1 of the Dairy Data Model, we will use the more common practice of GitFlow-style commits.
