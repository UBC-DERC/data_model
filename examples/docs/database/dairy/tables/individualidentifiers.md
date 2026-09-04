---
title: "individualidentifiers table"
description: "Linking individuals to external identifiers, such as websites, or ORCIDs."
---

# individualidentifiers
Description:

**Linking individuals to external identifiers, such as websites, or ORCIDs.**

## Columns

|        name        |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|--------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   *individualid*   |  uuid7 |                                                                                                                 An internal and unique identifier for an individual to support identification within the database.                                                                                                                |
|    *identifier*    |  text  |                                                                                                                               Text used as a valid identifier format (for example, DOIs or others).                                                                                                                               |
|*externaldatabaseid*|  uuid7 |                                                                                                                                  A unique internal identifier for an external database reference.                                                                                                                                 |
|    *datecreated*   |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
|   *datemodified*   |datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|

## Constraints

This table has no constraints

## Indexes

This table has no index

## Relationships

**References**

None.

**Referenced By**

None.
