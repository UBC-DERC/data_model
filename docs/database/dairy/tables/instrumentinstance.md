# instrumentinstance
Description:
**A particular instrument, with a particular location.**

## Columns

|  type  |    name    |                                                                                                                                                               comment                                                                                                                                                              |
|--------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| uuid-7 |instrumentid|                                             An internal, unique string to indentify a particular instrument in the general sense. This is as opposed to specific instances of an instrument which would be identified with both the broader instrument, and the specific serial number.                                            |
|  None  |    barn    |                                                                                                                                                                None                                                                                                                                                                |
|  None  |     pen    |                                                                                                                                                                None                                                                                                                                                                |
|  text  |  location  |                                                                                                 More specific description of the positioning within the pen/barn. For example, "Halfway down the long side of the pen, 2m height"
                                                                                                 |
|datetime| datecreated|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                |
|datetime|datemodified|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|

## Constraints

This table has no constraints

## Indexes


## Relationships

