# datasetpublications
Description:

**Links DERC related datasets to publications in the literature.**

## Columns

|      name     | type|                               comment                              |
|---------------|-----|--------------------------------------------------------------------|
|  *datasetid*  |uuid7|References the uuid for the dataset metadata stored in the database.|
|*publicationid*|uuid7|                A pointer to the publications table.                |

## Constraints

|                name                |    type   |                                                 def                                                 |                                         comment                                        |
|------------------------------------|-----------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
|  datasetpublications_datasetid_fk  |FOREIGN KEY|      FOREIGN KEY (datasetid) REFERENCES datasets(datasetid) ON UPDATE CASCADE ON DELETE CASCADE     |             The foreign key referencing the datasets table in the database.            |
|datasetpublications_publicationid_fk|FOREIGN KEY|FOREIGN KEY (publicationid) REFERENCES publication(publicationid) ON UPDATE CASCADE ON DELETE CASCADE|           The foreign key referencing the publications table in the database.          |
|    datasetpublications_joint_pk    |PRIMARY KEY|                                PRIMARY KEY (datasetid, publicationid)                               |The Primary Key here is the joint datasetid/publicationid key. It shouldn't be repeated.|

## Indexes

This table has no index

## Relationships

