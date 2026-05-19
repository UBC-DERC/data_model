# instruments
Description:
**A table for managing scientific and technical instruments used within the research system. This table is intended to help with connecting  measurements to documentation and workflow management. The design of this table and its associated foreign key links is based on the [RDA PIDINST v1.0](https://zenodo.org/records/6396467#.YkQxzRBBwlw).
**

## Columns

|   type   |           name          |                                                                                                                                                               comment                                                                                                                                                              |
|----------|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  uuid-7  |       instrumentid      |                                             An internal, unique string to indentify a particular instrument in the general sense. This is as opposed to specific instances of an instrument which would be identified with both the broader instrument, and the specific serial number.                                            |
|   text   |       description       |                                                                        A general description for the particular instrument that can be used to easily  identify the instrument. Should include a technical description of the device and its capabilities.
                                                                        |
|   text   |      instrumentname     |                                                                                                               The proper name by which the instrument is identified. The instrument may have other colloquial names.                                                                                                               |
|text array|instrumentcolloquialnames|                                                                                                              Colloquial names used for the instrument. This field should be a text array to support multiple entries.                                                                                                              |
|   None   |      manufacturerid     |                                                                                                                                                  The manufacturer of the product.                                                                                                                                                  |
|   None   |        supplierid       |                                                                                                                                     The organization through which the equipment was purchased.                                                                                                                                    |
| datetime |       datecreated       |                                 The date this entry was created. This field is used for the purposes of tracking changes across the database, and supporting reproducibility of data and data models, by allowing users to "roll back" or search for the impacts of new changes or data additions.
                                |
| datetime |       datemodified      |The date of the most recent record modification. This column does not identify how the record was changed, although this should be a central element of the data model. At present we are implementing the toolset, and providing the opportunity to see that a record was modified, not neccessarily how that record was modified.
|
|   UUID7  |   superceedingrecordid  |                                                                                                         In the case a record is replaced with an alternative record (for example a manufacturer is sold to a new company).                                                                                                         |

## Constraints

|       name      |    type   |                                                    def                                                    |                                                                                       comment                                                                                       |
|-----------------|-----------|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| instrument_pkey |PRIMARY KEY|                                         PRIMARY KEY (instrumentid)                                        |The PRIMARY KEY for this table is a UUID7, which is unordered and globally unique. This is not the same as the UPC or serial number, and should be used only for internal reference.
|
|superceeding_fkey|FOREIGN KEY|FOREIGN KEY (superceedingrecordid) REFERENCES instruments(instrumentid) ON UPDATE CASCADE ON DELETE CASCADE|                     In the event an instrument is re-defined somehow -- when a value is overwritten -- this hierarchical key will point to the new information.                     |
|manufacturer_fkey|FOREIGN KEY|           FOREIGN KEY (manufacturerid) REFERENCES institutions(institutionid) ON UPDATE CASCADE           |                                                                                         None                                                                                        |
|  supplier_fkey  |FOREIGN KEY|             FOREIGN KEY (supplierid) REFERENCES institutions(institutionid) ON UPDATE CASCADE             |                                                                                         None                                                                                        |

## Indexes


## Relationships

