# cows
Description:

**No comment present**

## Columns

|                                                                                                                                                               comment                                                                                                                                                              |     name     |  type  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|--------|
|                                                                                                                             This is the unique identifier given to the cow by the Canadian Government.                                                                                                                             |    *cadid*   |  text  |
|                                                           We clearly identify the scheme from which the cow ID is coming from. It is implied  that this is the Canadian data scheme, but if this data is used in synthesis work  it is important to identify the source.
                                                          | *cowschemeid*|  text  |
|                                                                     Within the UBC dairy the cows are given ear tags with the numbering scheme YNNN where Y is the last number of the year (6 for 2026) and NNN is the birth order of the cow in a given year.
                                                                    | *localcowid* | integer|
|                                                                                                                                      We record both male and female births in this database.
                                                                                                                                      |   *gender*   |nchar(1)|
|                                                                                                                                                   The weight of the cow at birth.                                                                                                                                                  | *birthweight*| integer|
|                                                                                                                     The cadid identifier for the dam. Should generally be constrained to be a valid identifer.
                                                                                                                    |    *damid*   |  text  |
|                                                                                                                     My guess is that this is actually a pointer to another table, with some extra information.
                                                                                                                    |   *sireid*   |  text  |
|                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                | *datecreated*|datetime|
|The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|*datemodified*|datetime|

## Constraints

|    name   |          type         |               def              |                                                                 comment                                                                 |
|-----------|-----------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
|cowuniqueid|      PRIMARY KEY      |PRIMARY KEY (cadid, cowschemeid)|The PRIMARY KEY for this table is the unique set of the Canadian ID and the scheme type. In our case all of the identifiers should have 
|
| damidvalid|CHECK (damid ~* '^.*$')|              None              |                     A constraint to ensure that the dam ID is a valid ID based on the Canadian government ID scheme.                    |

## Indexes


## Relationships

