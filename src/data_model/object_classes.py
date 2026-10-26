from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class extensible_dict(BaseModel):
    """Supporting the use of `x-` extensions for the data model. This will
    support links to external schema (for example)."""

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "patternProperties": {"^x-": {}},
            "additionalProperties": False,
        },
    )

    @model_validator(mode="after")
    def _validate_extensions(self):
        for key in self.model_extra or {}:
            if key.startswith("x-"):
                continue
            raise ValueError(
                f"Invalid extension key '{key}'; all extensions must start with 'x-'"
            )
        return self


class column_dict(extensible_dict):
    """A class for columns, supporting the use of `x-` extensions for the data model."""

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
    Default ON UPDATE and ON DELETE actions (`None`) is an implied `NO ACTION` (the
    Postgres default when no statement follows).
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    schema_: str | None = Field(default=None, alias="schema")
    table: str | None = None
    columns: list[str]
    on_update: OnUpdateType | None = None
    on_delete: OnDeleteType | None = None


class ConstraintType(str, Enum):
    """Allowed PostgreSQL constraint types."""

    check = "CHECK"
    unique = "UNIQUE"
    unique_nulls_not_distinct = "UNIQUE NULLS NOT DISTINCT"
    primary_key = "PRIMARY KEY"
    foreign_key = "FOREIGN KEY"
    exclude = "EXCLUDE"


class constraint_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    type: ConstraintType
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
        if self.references is not None and self.references.table is None:
            raise ValueError(
                f"constraint '{self.name}' has a references block but no table "
                f"defined; a table must be specified."
            )
        return self

    @model_validator(mode="after")
    def columns_must_be_defined_for_constraints(self):
        if len(self.columns) == 0:
            raise ValueError(
                f"constraint '{self.name}' is type {self.type!r} but has no columns "
                f"defined; at least one column must be specified."
            )
        return self

    @model_validator(mode="after")
    def columns_defined_must_have_same_count_as_columns_referenced(self):
        ref_cols = self.references.columns if self.references else []
        if self.type == ConstraintType.foreign_key and len(self.columns) != len(
            ref_cols
        ):
            raise ValueError(
                f"constraint '{self.name}' references {len(ref_cols)} columns, but ",
                f"has {len(self.columns)!r} defined.",
            )
        return self


class index_dict(BaseModel):
    # Indexes are always defined on their owning table, so they carry only
    # local ``columns`` — there is no cross-table reference to validate.
    model_config = ConfigDict(extra="forbid")
    name: str
    type: str | None = None
    comment: str = "No comment provided."
    ddl: str | None = None
    columns: list[str] = []


class table_dict(extensible_dict):
    # ``schema`` is advisory only; a table's owning schema is authoritative via
    # its folder placement and membership in a schema_dict. Stored as
    # ``schema_`` (aliased to ``schema``) to avoid shadowing BaseModel.schema().
    model_config = ConfigDict(populate_by_name=True)
    name: str
    schema_: str | None = Field(default=None, alias="schema")
    type: str = "BASE TABLE"
    comment: str | None = "No comment provided."
    columns: list[column_dict]
    constraints: list[constraint_dict] = []
    indexes: list[index_dict] = []


class schema_dict(extensible_dict):
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
    schemas: list[schema_dict] = []


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
    summary: str = "No summary provided."
    license: license_dict = license_dict(full_name="Default Copyright Applies")
    contacts: list[contact_dict] = []


class ddaml_dict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ddaml_version: str
    database: DDL_Dict
    info: ddaml_info
