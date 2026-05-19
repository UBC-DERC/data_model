# cows
Description:
**No comment present**

## Columns

|  type  |    name    |                                                                                                                                                               comment                                                                                                                                                              |
|--------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  text  |    cadid   |                                                                                                                             This is the unique identifier given to the cow by the Canadian Government.                                                                                                                             |
|  text  | cowschemeid|                                                           We clearly identify the scheme from which the cow ID is coming from. It is implied  that this is the Canadian data scheme, but if this data is used in synthesis work  it is important to identify the source.
                                                          |
| integer| localcowid |                                                                     Within the UBC dairy the cows are given ear tags with the numbering scheme YNNN where Y is the last number of the year (6 for 2026) and NNN is the birth order of the cow in a given year.
                                                                    |
|nchar(1)|   gender   |                                                                                                                                      We record both male and female births in this database.
                                                                                                                                      |
| integer| birthweight|                                                                                                                                                   The weight of the cow at birth.                                                                                                                                                  |
|  text  |    damid   |                                                                                                                     The cadid identifier for the dam. Should generally be constrained to be a valid identifer.
                                                                                                                    |
|  text  |   sireid   |                                                                                                                     My guess is that this is actually a pointer to another table, with some extra information.
                                                                                                                    |
|datetime| datecreated|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                |
|datetime|datemodified|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|

## Constraints

|    name   |          type         |               def              |                                                                 comment                                                                 |
|-----------|-----------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
|cowuniqueid|      PRIMARY KEY      |PRIMARY KEY (cadid, cowschemeid)|The PRIMARY KEY for this table is the unique set of the Canadian ID and the scheme type. In our case all of the identifiers should have 
|
| damidvalid|CHECK (damid ~* '^.*$')|              None              |                     A constraint to ensure that the dam ID is a valid ID based on the Canadian government ID scheme.                    |

## Indexes


## Relationships

