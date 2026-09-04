---
title: "instrumentowners table"
description: "Which person or organization (or both) maintains ownership of this instrument?"
---

# instrumentowners
Description:

**Which person or organization (or both) maintains ownership of this instrument?**

## Columns

|      name     |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|---------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *instrumentid*| uuid-7 |                                            An internal, unique string to indentify a particular instrument in the general sense. This is as opposed to specific instances of an instrument which would be identified with both the broader instrument, and the specific serial number.                                            |
| *individualid*|  uuid7 |                                                                                                                 An internal and unique identifier for an individual to support identification within the database.                                                                                                                |
|*institutionid*|  UUID7 |                                                                                                                                        The unique internal identifier for the institution.                                                                                                                                        |
| *datecreated* |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
| *datemodified*|datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|

## Constraints

This table has no constraints

## Indexes

This table has no index

## Relationships

**References**

None.

**Referenced By**

None.
