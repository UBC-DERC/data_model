# DDAML Specification

This document serves to define the specifications for the DDAML (Database Description Ain't Markup Language) format that will be used to generate valid (Postgres) data description language (DDL) structure through the [`data_model`](https://gituhb.com/UBC-DERC/data_model) and the [`ddl_builder`](https://github.com/UBC-DERC/ddl_builder) Python packages. The goal is to develop a human readable document format that can be processed by a Python script and transformed into usable SQL to work within a system in which ATOMic features of databases are required, but schema or data model specifications may change over time.

This format will attempt to mirror other existing schema, and is strongly influenced by [OpenAPI](https://spec.openapis.org/oas/latest.html).

## Version 2026.10

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC2119](https://www.rfc-editor.org/info/rfc2119/).

### Introduction

This documentation is intended to support a data model that allows users to read, build documentation, and itterate over data models for (Postgres) databases over time as part of a workflow that allows lay partners and technical experts to work together to develop and define appropriate data models for complex systems. The tool was originally developed as part of work at the University of British Columbia's Dairy Education and Research Center, where multiple existing systems, proprietary data models, and a history of academic research resulted in a large number of heterogenous datasets that needed to be aligned to support longitudinal data analysis.

The models and systems established as part of DDAML allow system developers to consult with domain experts, technicians, researchers and other invested groups, without the need for deep understanding of underlying database principles. It allows for integrated development of indices, constraints and references, and can support the implementation of best-practices early on in the database design process.

### Versioning System

Versioning will use a [CalVer](https://calver.org/) system, using a YYYY.M.D.MICRO format without padding. Breaking changes will be documented in the CHANGELOG, and end-of-support will be documented in the specifications and in the README.

## Objects

### Fixed Fields

| Field name | Type | Description |
| --- | --- | --- |
| ddaml | str | REQUIRED. This string MUST be the CalVer version number of the ddaml specification. This field allows other tooling to understand the structure and specification of the ddaml file. |
| info | str | REQUIRED. This string is used to provide additional metadata about the purpose of the ddaml document and data model. |

### Database

| Field name | Type | Description |
| --- | --- | --- |
| encoding | str | 'UTF8' |
| locale | str | 'en_CA' |
| name | str | |
| owner | str | None = None |
| comment | str | "No comment provided." |
| extensions | list[str] | [] |
| schemas | [Schema Objects](#schema) | |

### Schema

| Field name | Type | Description |
| --- | --- | --- |

### Table

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. The name given to the table. It MUST conform to existing naming conventions for the database target (currently only Postgres). |
| schema | str | The schema within which the table exists. This may be inherited, or explicitly defined. |
| type | str | The type of table (allowing extension to BASE TABLE, VIEW and other types of table structures within Postgres). |
| comment | str | A string comment to describe the table. Used as part of the `COMMENT` clause in SQL. Default is and empty string that will not be added as a comment. |
| columns | [Column Object](#column) | Zero or more Column objects, in a list. |
| constraints | [Constraint Object](#constraint) | Zero or more constraint objects in a list. |
| indexes | [Index Object](#index) | Zero or more Index objects in a list |

### Column

| Field name | Type | Description |
| --- | --- | --- |
| name | str | The formal column name. Should conform to Postgres standard. |
| type | str | Column type. MUST conform to an allowed [Postgres data type](https://www.postgresql.org/docs/current/datatype.html) or a type supported by an existing Postgres extension. Validation occurs during converstion to DDL in the `ddl_builder` Python package. |
| comment | str | As opposed to the [Table Object](#table) comments, the column comments default to "No comment provided." |
| nullable | bool | Is the field nullable? Defaults to `True` |
| default | str | Defines a default value, the field is submitted as a string, but will be transformed based on the `type` defined above. |

### Index

| Field name | Type | Description |
| --- | --- | --- |

### Constraint

| Field name | Type | Description |
| --- | --- | --- |
