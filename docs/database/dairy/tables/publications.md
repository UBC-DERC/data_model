---
title: "publications table"
description: "Documenting publication information tied to DERC. May be related to DERC researchers, collaborators or associated work. This table is likely to be liberal in..."
---

# publications
Description:

**Documenting publication information tied to DERC. May be related to DERC researchers, collaborators or associated work. This table is likely to be liberal in its inclusion because much of the material will be imported through bulk-import processes.**

## Columns

|        name        |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|--------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   *publicationid*  |  uuid7 |                                                                                                                                   A unique internal identifer for a publication in the database.                                                                                                                                  |
|       *title*      |  text  |                                                                                                                                                 The article, or publication title.                                                                                                                                                |
|     *abstract*     |  text  |                                                                                                                                             A longer form description of the dataset.                                                                                                                                             |
|    *datecreated*   |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
|   *datemodified*   |datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|
|      *bibtex*      |  jsonb |                                                                                                                                            A valid BibTeX reference for a publication.                                                                                                                                            |
|*datepublishedstart*|datetime|                                              A datetime object for the beginning of the publication date. We use start and end date as a convention to manage uncertainty. In a case where only year is known, we assign dates beginning at XXXX-01-01 and an end date of XXXX-12-31.                                             |
| *datepublishedend* |datetime|                                            A datetime object for the end of the possible publication date. We use start and end date as a convention to manage uncertainty. In a case where only year is known, we assign dates beginning at XXXX-01-01 and an end date of XXXX-12-31.                                            |

## Constraints

|     name     |    type   |            ddl            |       comment      |
|--------------|-----------|---------------------------|--------------------|
|publication_pk|PRIMARY KEY|PRIMARY KEY (publicationid)|No comment provided.|

## Indexes

This table has no index

## Relationships

