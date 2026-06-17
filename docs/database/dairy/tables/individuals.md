# individuals
Description:

**The primary table for storing records about an individual. We are modeling this table after the [schema:Person](https://schema.org/Person) data model to some degree, for broader compatibility.**

## Columns

|         name         |  type  |                                                                                                                                                              comment                                                                                                                                                              |
|----------------------|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|    *individualid*    |  uuid7 |                                                                                                                 An internal and unique identifier for an individual to support identification within the database.                                                                                                                |
|      *fullname*      |  text  |                                                                                                                        Full name of an individual, in written order (i.e., as they would write their names)                                                                                                                       |
|     *formalname*     |  text  |                                                                                             This is the last name, family name, or singular name that would lead in a journal citation, or when the individual is formally addressed.                                                                                             |
|    *preferredname*   |  text  |                                                                                                                        For individuals who have a preferred name that is not the same as their given name.                                                                                                                        |
|     *datecreated*    |datetime|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                |
|    *datemodified*    |datetime|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.|
|*superceedingrecordid*|  UUID7 |                                                                                  In the case a record is replaced with an alternative record (for example an individual changes their name, but the "old" name remains in the publication list).                                                                                  |

## Constraints

|     name    |    type   |           def           |                           comment                          |
|-------------|-----------|-------------------------|------------------------------------------------------------|
|individual_pk|PRIMARY KEY|PRIMARY KEY(individualid)|The primary key for the table (comes with indexing as well).|

## Indexes

This table has no index

## Relationships

