# datasets
Description:

**A table to document datasets associated with the UBC Dairy Research Farm.
Modeled largely on the work of [Science On Schema](https://github.com/ESIPFed/science-on-schema.org/blob/main/guides/Dataset.md)
**

## Columns

|                                                                                                                                                               comment                                                                                                                                                              |        name        |  type  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|--------|
|      A unique internal indentifier for the dataset. This dataset id is used to link to records and objects internally within the database. We use a uuid7 data type for these records so that the identifier can be located across all data tables (as opposed to an integer, which may be duplicated across multiple tables).     |     *datasetid*    |  uuid7 |
|                                                                                                                                    A short name for the dataset used in summarizing its content.                                                                                                                                   |    *datasetname*   |  text  |
|                                                                                                                                              A longer form description of the dataset.                                                                                                                                             |*datasetdescription*|  text  |
|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                |    *datecreated*   |datetime|
|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|   *datemodified*   |datetime|

## Constraints

|    name   |    type   |          def          |comment|
|-----------|-----------|-----------------------|-------|
|datasets_pk|PRIMARY KEY|PRIMARY KEY (datasetid)|  None |

## Indexes


## Relationships

