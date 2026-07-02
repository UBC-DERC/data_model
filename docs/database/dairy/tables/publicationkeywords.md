---
title: "publicationkeywords table"
description: "Linking publications to associated keywords."
---

# publicationkeywords
Description:

**Linking publications to associated keywords.**

## Columns

|      name     |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|---------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|*publicationid*|  uuid7 |                                                                                                                                   A unique internal identifer for a publication in the database.                                                                                                                                  |
|  *keywordid*  |  uuid7 |                                                                                                                               A unique internal identifer for a keyword/source pair in the database.                                                                                                                              |
|   *sourceid*  |  uuid7 |                                                                               A unique internal indentifier for an external source for subjects or keywords. This may include sources such as WikiData, or the Library of Congress subject catalog.                                                                               |
| *datecreated* |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
| *datemodified*|datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|

## Constraints

|      name      |    type   |                                         ddl                                        |       comment      |
|----------------|-----------|------------------------------------------------------------------------------------|--------------------|
|publication_fkey|FOREIGN KEY|FOREIGN KEY (publicationid) REFERENCES publications(publicationid) ON UPDATE CASCADE|No comment provided.|
|  keyword_fkey  |FOREIGN KEY|      FOREIGN KEY (keywordid) REFERENCES keywords(keywordid) ON UPDATE CASCADE      |No comment provided.|

## Indexes

This table has no index

## Relationships

