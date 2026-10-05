# DDAML Specification
Date: October 5, 2026

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
| database | [Database object](#database) | REQUIRED. The database definition |

### Info

These fields are similar to the fields defined in the [OpenAPI v3.2.1 Specification](https://spec.openapis.org/oas/v3.2.1.html). They are used to support metadata propagation for specific data models, and to identify the rights owner, and data or object discovery.

| Field name | Type | Description |
| --- | --- | --- |
| title | str | REQUIRED. The title of the data model (different from the database name). This is a formal title for the document. |
| summary | str | A short summary of the database model. |
| description | str | A description of the data model. [CommonMark](https://commonmark.org/) syntax MAY be used for rich text representation. |
| contact | [[Contact Object](#contact)] | The contact information for the metadata and data model maintainer. |
| license | [License Object](#license) | The license information for the data model and structured repository associated with it. |
| version | str | REQUIRED. The version of the DDAML document (which is distinct from the DDAML Specification version). |

### Contact

Support for contact information. Drawn from the OpenAPI standard.

| Field name | Type | Description |
| --- | --- | --- |
| name | str | The identifying name of the contact person/organization. |
| url | str | The URI for the contact information. This MUST be in the form of a URI. |
| email | str | The email address of the contact person/organization. This MUST be in the form of an email address. |

### License

A field to support the discovery and application of licensing to any data model created using a DDAML form/format.

| Field name | Type | Description |
| --- | --- | --- |
| name | str | REQUIRED. The license name used for the data model. |
| identifier | str | An [SPDX-Licenses](https://spdx.org/licenses/) expression for the API. The identifier field is mutually exclusive of the url field. |
| url | str | A URI for the license used for the data model. This MUST be in the form of a URI. The url field is mutually exclusive of the identifier field. |

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
| name | str | REQUIRED. A valid schema name. |
| comment | str | A comment to apply to the schema. The default value is "No comment provided." |
| tables | [Table objects](#table) | [] |

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
