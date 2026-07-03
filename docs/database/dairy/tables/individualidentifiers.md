# individualidentifiers
Description:

**Linking individuals to external identifiers, such as websites, or ORCIDs.**

## Columns

|                                                                                                                                                               comment                                                                                                                                                              |        name        |  type  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|--------|
|                                                                                                                 An internal and unique identifier for an individual to support identification within the database.                                                                                                                 |   *individualid*   |  uuid7 |
|                                                                                                                                Text used as a valid identifier format (for example, DOIs or others).                                                                                                                               |    *identifier*    |  text  |
|                                                                                                                                  A unique internal identifier for an external database reference.                                                                                                                                  |*externaldatabaseid*|  uuid7 |
|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                |    *datecreated*   |datetime|
|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|   *datemodified*   |datetime|

## Constraints

This table has no constraints

## Indexes

This table has no index

## Relationships

