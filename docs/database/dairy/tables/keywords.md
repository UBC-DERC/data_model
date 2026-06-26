---
title: "keywords table"
description: "A table for keywords for datasets, publications and other terms. Ideally these terms are linked to external resources, such as ontologies or subject schema."
---

# keywords
Description:

**A table for keywords for datasets, publications and other terms. Ideally these terms are linked to external resources, such as ontologies or subject schema.**

## Columns

|        name        |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|--------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   *publicationid*  |  uuid7 |                                                                                                                               A unique internal identifer for a keyword/source pair in the database.                                                                                                                              |
|      *keyword*     |  text  |                                                                                                                                        A keyword used to describe a thing in the database.                                                                                                                                        |
|     *sourceid*     |  uuid7 |                                                                               A unique internal indentifier for an external source for subjects or keywords. This may include sources such as WikiData, or the Library of Congress subject catalog.                                                                               |
|    *datecreated*   |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
|   *datemodified*   |datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|
|*superceedingrecord*|  UUID7 |                                                                                                         In the case a record is replaced with an alternative record (for example a manufacturer is sold to a new company).                                                                                                        |

## Constraints

|    name    |    type   |               ddl              |                         comment                         |
|------------|-----------|--------------------------------|---------------------------------------------------------|
|keywordid_pk|PRIMARY KEY|PRIMARY KEY(keywordid, sourceid)|Primary key for the keywords table (expects to be unique)|

## Indexes

This table has no index

## Relationships

