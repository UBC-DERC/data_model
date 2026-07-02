from pydantic import BaseModel, ConfigDict, Field

class column_dict(BaseModel):
    name:str
    type:str
    comment:str = "No comment provided."
    nullable:bool = True

class reference_dict(BaseModel):
    # ``schema`` shadows BaseModel.schema(), so store it as ``schema_`` while
    # keeping the YAML/serialised key as ``schema`` via an alias. schema/table
    # are optional and are filled from the owning table's context during the
    # resolution pass (see check_references.resolve_references).
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    schema_:str | None = Field(default=None, alias="schema")
    table:str | None = None
    columns:list[str]

class constraint_dict(BaseModel):
    name:str
    type:str | None = None
    comment:str = "No comment provided."
    ddl:str | None = None
    reference: list[reference_dict] = []

class index_dict(BaseModel):
    name:str
    type:str | None = None
    comment:str = "No comment provided."
    ddl:str
    reference:list[reference_dict] = []

class table_dict(BaseModel):
    name:str
    type:str = 'BASE TABLE'
    comment:str = "No comment provided."
    columns:list[column_dict]
    constraints:list[constraint_dict] = []
    indexes:list[index_dict] = []

class schema_dict(BaseModel):
    name:str
    comment:str = "No comment provided."
    tables:list[table_dict]

class DDL_Dict(BaseModel):
    encoding:str = 'UTF8'
    locale:str = 'en_CA'
    name:str
    comment:str = "No comment provided."
    extensions:list[str] = []
    schemas:list[schema_dict]
