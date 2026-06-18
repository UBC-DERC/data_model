# externaldatabases
Description:

**A table to manage and record pointers to various external resources. These resources include data management tools such as DOIs and ARKs, product identifiers such as UPC codes,  and other external references such as WikiData, or others.**

## Columns

|                                                                                                                                                                                                                                 comment                                                                                                                                                                                                                                |  type  |        name        |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------------------|
|                                                                                                                                                                                                    A unique internal identifier for an external database reference.                                                                                                                                                                                                    |  uuid7 |*externaldatabaseid*|
|                                                                                                                                                                                                           The name of the external database or data resource.                                                                                                                                                                                                          |  text  | *externaldatabase* |
|                                                                                                                                                                                                          A web address for this resource, a primary location.                                                                                                                                                                                                          |   url  |        *url*       |
|The url mask is intended to show how the identifers should be used.  The mask will be based on the resource itself. For example, ORCID indicates  that its identifiers should be written as `https://orcid.org/0000-0000-0000-0000`,  in which case the URL mask should be `{identifier}` such that replacing the  identifier produces a valid URL. Thus, for a DOI, where the DOI itself is written `10.0000/0000000`, the mask will be `https://doi.org/{identifier}`.|   url  |      *urlmask*     |
|                                                                                                   The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.                                                                                                   |datetime|    *datecreated*   |
|                                                                   The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.                                                                  |datetime|   *datemodified*   |

## Constraints

This table has no constraints

## Indexes

This table has no index

## Relationships

