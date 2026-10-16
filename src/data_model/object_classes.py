from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class column_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: str
    comment: str = "No comment provided."
    nullable: bool = True
    default: str | None = None


class OnUpdateType(str, Enum):
    """Allowed PostgreSQL ON UPDATE actions."""

    no_action = "NO ACTION"
    restrict = "RESTRICT"
    cascade = "CASCADE"
    set_null = "SET NULL"
    set_default = "SET DEFAULT"


class OnDeleteType(str, Enum):
    """Allowed PostgreSQL ON DELETE actions."""

    no_action = "NO ACTION"
    restrict = "RESTRICT"
    cascade = "CASCADE"
    set_null = "SET NULL"
    set_default = "SET DEFAULT"


class reference_dict(BaseModel):
    """Reference structure for the data model.
    By default the reference is assumed to be in the same schema as the owning table
    Default ON UPDATE and ON DELETE actions are NO ACTION unless specified otherwise.
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    schema_: str | None = Field(default=None, alias="schema")
    table: str | None = None
    columns: list[str]
    on_update: OnUpdateType = OnUpdateType.no_action
    on_delete: OnDeleteType = OnDeleteType.no_action


class ConstraintType(str, Enum):
    """Allowed PostgreSQL constraint types."""

    check = "CHECK"
    unique = "UNIQUE"
    unique_nulls_not_distinct = "UNIQUE NULLS NOT DISTINCT"
    primary_key = "PRIMARY KEY"
    foreign_key = "FOREIGN KEY"
    none = "NONE"


class constraint_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: ConstraintType = ConstraintType.none
    comment: str = "No comment provided."
    ddl: str | None = None
    columns: list[str] = []
    references: reference_dict | None = None

    @model_validator(mode="after")
    def _references_only_on_foreign_keys(self):
        if self.references is not None and self.type != ConstraintType.foreign_key:
            raise ValueError(
                f"constraint '{self.name}' has a references block but is type "
                f"{self.type!r}; only FOREIGN KEYs may reference another table."
            )
        return self

    @model_validator(mode="after")
    def _references_must_have_columns(self):
        if self.references is not None and not self.references.columns:
            raise ValueError(
                f"constraint '{self.name}' has a references block but no columns "
                f"defined; at least one column must be specified."
            )
        return self

    @model_validator(mode="after")
    def _references_must_have_table(self):
        if self.references is not None and not self.references.table:
            raise ValueError(
                f"constraint '{self.name}' has a references block but no table "
                f"defined; a table must be specified."
            )
        return self

    @model_validator(mode="after")
    def colums_must_be_defined_for_constraints(self):
        if self.type != ConstraintType.none and len(self.columns) == 0:
            raise ValueError(
                f"constraint '{self.name}' is type {self.type!r} but has no columns "
                f"defined; at least one column must be specified."
            )
        return self


class index_dict(BaseModel):
    # Indexes are always defined on their owning table, so they carry only
    # local ``columns`` — there is no cross-table reference to validate.
    model_config = ConfigDict(extra="forbid")
    name: str
    type: str | None = None
    comment: str = "No comment provided."
    ddl: str
    columns: list[str] = []


class table_dict(BaseModel):
    # ``schema`` is advisory only; a table's owning schema is authoritative via
    # its folder placement and membership in a schema_dict. Stored as
    # ``schema_`` (aliased to ``schema``) to avoid shadowing BaseModel.schema().
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    name: str
    schema_: str | None = Field(default=None, alias="schema")
    type: str = "BASE TABLE"
    comment: str | None = "No comment provided."
    columns: list[column_dict]
    constraints: list[constraint_dict] = []
    indexes: list[index_dict] = []


class schema_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    comment: str = "No comment provided."
    tables: list[table_dict] = []


class DDL_Dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    encoding: str = "UTF8"
    locale: str = "en_CA"
    name: str
    owner: str | None = None
    comment: str = "No comment provided."
    extensions: list[str] = []
    schemas: list[schema_dict]


class license_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: str
    licenseId: str | None = None
    url: str | None = None


class contact_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    email: str | None = None
    url: str | None = None


class ddaml_info(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str
    title: str
    summary: str
    license: license_dict
    contacts: list[contact_dict] = []


class ddaml_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    database: DDL_Dict
    info: ddaml_info
