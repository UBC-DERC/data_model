---
title: "datasetidentifiers table"
description: "Links datasets to URLs/DOIs/ARKs for external data resources."
---

# datasetidentifiers
Description:

**Links datasets to URLs/DOIs/ARKs for external data resources.**

## Columns

|        name        |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|--------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     *datasetid*    |  uuid7 |     A unique internal indentifier for the dataset. This dataset id is used to link to records and objects internally within the database. We use a uuid7 data type for these records so that the identifier can be located across all data tables (as opposed to an integer, which may be duplicated across multiple tables).     |
|    *identifier*    |  text  |                                          The external identifier for the dataset object. This may be a DOI,  an ARK or a different data object. Currently the choice is simply  one of the entries in the `externaldatabases` table, but this may  be limited to a subset in the future.                                          |
|*externaldatabaseid*|  uuid7 |                                      A pointer to the `externaldatabase` table. It may be worth adding a constraint that the `identifier` and the `urlmask` should form a valid URL. In this case we should do some proper error/assertion responses to make sure we're getting things right.                                     |
|    *datecreated*   |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
|   *datemodified*   |datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|

## Constraints

|               name               |    type   |                                                         ddl                                                         |                       reference                      |                                                  comment                                                  |
|----------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
|       datasetidentifiers_pk      |PRIMARY KEY|                               PRIMARY KEY (datasetid, identifier, externaldatabaseid)                               |                                                      |Primary key to ensure unique entries. Joint key, since we need all the information to provide a unique key.|
|    datasetidentifiers_dsid_fk    |FOREIGN KEY|              FOREIGN KEY (datasetid) REFERENCES datasets(datasetid) ON UPDATE CASCADE ON DELETE CASCADE             |          [datasets](datasets.md) (datasetid)         |                                 A foreign key to point to the dataset id.                                 |
|datasetidentifiers_externaldbid_fk|FOREIGN KEY|FOREIGN KEY (externaldatabaseid) REFERENCES externaldatabases(externaldatabaseid) ON UPDATE CASCADE ON DELETE CASCADE|[externaldatabases](externaldatabases.md) (databaseid)|                         Foreign key reference to external databases or resources.                         |

## Indexes

This table has no index

## Relationships

**References**

*  → [datasets](datasets.md) (`datasetid`)
*  → [externaldatabases](externaldatabases.md) (`databaseid`)

**Referenced By**

None.
