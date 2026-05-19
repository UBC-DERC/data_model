# institutions
Description:

**A table for institutions and organizations. This table is modeled after the [Research Organization Registry](https://ror.org/) and is
intended to link to collaboration institutions, manufacturers, suppliers and research or operational dairy farms.
**

## Columns

|                                                                                                                                                               comment                                                                                                                                                              |        name        |  type  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|--------|
|                                                                                                                                         The unique internal identifier for the institution.                                                                                                                                        |   *institutionid*  |  UUID7 |
|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                |    *datecreated*   |datetime|
|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|   *datemodified*   |datetime|
|                                                                                                         In the case a record is replaced with an alternative record (for example a manufacturer is sold to a new company).                                                                                                         |*superceedingrecord*|  UUID7 |

## Constraints

This table has no constraints

## Indexes


## Relationships

