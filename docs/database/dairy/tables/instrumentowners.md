# instrumentowners
Description:

**Which person or organization (or both) maintains ownership of this instrument?**

## Columns

|                                                                                                                                                               comment                                                                                                                                                              |      name     |  type  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|--------|
|                                             An internal, unique string to indentify a particular instrument in the general sense. This is as opposed to specific instances of an instrument which would be identified with both the broader instrument, and the specific serial number.                                            | *instrumentid*| uuid-7 |
|                                                                                                                                                                None                                                                                                                                                                |  *contactid*  |  None  |
|                                                                                                                                                                None                                                                                                                                                                |*institutionid*|  None  |
|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                | *datecreated* |datetime|
|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
| *datemodified*|datetime|

## Constraints

This table has no constraints

## Indexes


## Relationships

