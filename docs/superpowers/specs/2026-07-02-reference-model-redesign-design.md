# Reference model redesign

## Context

The data model stores PostgreSQL definitions as structured YAML. A second
repository turns the composite `output.yaml` into a runnable DDL script. Within
each constraint, a hand-written `ddl` string carries the authoritative SQL,
because reconstructing every SQL clause from structure in the downstream tool is
too complex.

The structured fields exist for two reasons:

1. To help users who are **not** proficient in SQL build data models.
2. To let this tool **validate references** — both *within* a table (do the
   named columns exist?) and *across* tables (does the referenced table and its
   columns exist?).

Reference validation is the critical capability. Validating the `ddl` string
itself is out of scope.

## Problem

A single `reference: [{schema, table, columns}]` block is overloaded across
unlike constraint types, and `columns` means different things in different
places:

| Constraint | Needs | Current `reference` |
|---|---|---|
| `PRIMARY KEY (cadid, cowschemeid)` | local columns | fake self-reference to `cows` |
| `FOREIGN KEY (supplierid) REFERENCES institutions(institutionid)` | local cols + target table + target cols | `table: institutions, columns: [supplierid]` — target column `institutionid` is lost, `columns` holds the *local* column |
| `CHECK (damid ~* '...')` | the columns it touches | fabricated reference to `cows` |

The referenced column and referential actions live only in the `ddl` string, so
the structured form cannot be validated reliably. This is a modeling problem:
the class structure must stop conflating "local columns" with "foreign target."

## Design

### `reference_dict` — a foreign target with context-defaulted location

- `schema` — optional. Absent → the **owning table's schema**.
- `table` — optional. Absent → the **owning table**.
- `columns` — required. The **referenced** columns, validated against the
  resolved target table.

Defaults are filled by a resolution pass after the model loads, so the composite
`output.yaml` is fully qualified for the downstream repo. An `table` value that
is *provided but resolves to no table* is an **error**, never silently
reassigned to the owning table. Defaulting applies only to omitted keys.

A `references.table` that defaults to the owning table expresses a
**self-referential foreign key** (e.g. `cows.damid → cows.cadid`).

### Constraint class — one shape plus a validator (approach "B'")

Fields:

- `name`, `type` (`PRIMARY KEY` / `FOREIGN KEY` / `UNIQUE` / `CHECK`),
  `comment`, `ddl` (authoritative SQL, kept).
- `columns` — the constraint's **own/local** columns, validated against the
  owning table. Used by PK, UNIQUE, the local side of FK, and the columns a
  CHECK touches.
- `references` — **optional** foreign target (above). A `model_validator`
  permits it **only** when `type == FOREIGN KEY`; CHECK and PK cannot carry one.

A single shape keeps YAML authoring simple for non-SQL users while the validator
rejects illegal combinations at load time.

### Resolution and validation

A pass walks schemas → tables → constraints and:

1. Fills each `references` default `schema`/`table` from the owning table.
2. Checks every constraint's local `columns` exist in the owning table.
3. Checks every `references` target `(schema, table)` exists and its `columns`
   exist there.

All problems are collected and reported together at the end (current behaviour),
never raising on the first failure.

### Indexes

Drop the unused foreign `reference` field; keep local `columns` only. No index
definitions exist yet, so there is no migration.

### YAML data migration is out of scope (owned by the maintainer)

The `data_definitions/` YAML files are maintained by hand. This work touches
**Python and `validation.yaml` only**; it does not modify any data YAML. The
maintainer migrates the constraint blocks manually to the new shape:

- PK / CHECK: no `references`; local `columns` listed.
- FK: local `columns`, plus a `references` whose `columns` are the *referenced*
  columns (e.g. `supplier_fkey → columns: [supplierid], references: {table: institutions, columns: [institutionid]}`).

Until the data YAML is migrated, loading the real model is expected to fail:
phase 1 (pydantic `extra='forbid'` + the constraint validator) rejects the old
`referencedTable` / `referencedColumns` / list-style `reference` keys, and
phase 2 reports any unresolved references. That surfacing of errors is the
intended behaviour, not a regression.

## Testing

- `reference_dict`: schema/table optional, columns required.
- Resolution: omitted schema/table default to owning context; wrong names are
  left unresolved (so checking flags them).
- Constraint validator: `references` accepted for FK, rejected for CHECK/PK.
- Reference checking: local columns must exist in the owning table; FK target
  table and referenced columns must exist; all failures collected and reported
  together.
- Integration: the real model loads, resolves, and passes reference checking.

## Out of scope

- Modifying any `data_definitions/` YAML file (maintainer-owned, migrated by hand).
- Validating or generating the `ddl` string.
- Referential actions (`ON UPDATE` / `ON DELETE`) in the structured model.
- New constraint types beyond PK / FK / UNIQUE / CHECK.
