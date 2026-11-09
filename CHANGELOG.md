# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) using a YYYY-MM model.

## [2026-11-alpha]

### Added

- **DDAML specification** (`docs/specifications/SPECIFICATION.md`, v2026.10.26) defining the
  document structure, now linked from the docs navigation.
- **`ddaml_dict` root model** wrapping the database definition with document metadata:
  - `ddaml_version` (required): the CalVer version of the DDAML specification.
  - `info` block (`ddaml_info`) with `title`, `version`, `summary`, `license` and `contacts`.
  - `license_dict` (`full_name` plus `licenseId` and/or `url`) and `contact_dict`
    (`name`, `email`, `url`), with URL and email validation via the `validators` package.
- **`x-` extension keys** allowed on schemas, tables and columns (`extensible_dict`); any
  other unknown key is rejected.
- `on_update` / `on_delete` actions on foreign-key `references` blocks, using a single
  `OnChangeType` enum (`NO ACTION`, `RESTRICT`, `CASCADE`, `SET NULL`, `SET DEFAULT`).
- `EXCLUDE` constraint type.
- New constraint validators: every constraint must list columns; a `references` block must
  name a table and at least one column; foreign keys must reference the same number of
  columns they define.
- `data_model.json_schema` module (`build_schema()`, `write_schema()`); the schema now
  declares `$schema` (JSON Schema 2020-12) and `$id`.
- `.pre-commit-config.yaml` (ruff check/format and `ty`), with `pre-commit` added as a dev
  dependency.
- Tests for the `info` block, `x-` extensions, cross-references and the new validators.

### Changed

- **Breaking:** entry files must now contain a top-level `database:` block alongside
  `ddaml_version` and `info`; `load_database()` returns a `ddaml_dict` and raises
  `ModelValidationError` when the `database:` block is missing.
- **Breaking:** foreign-key `references` must name the target `table` explicitly. An omitted
  table no longer defaults to a self-reference (an omitted `schema` still defaults to the
  owning schema).
- Constraint `type` is now required (it can no longer be `None`).
- Reference actions are no longer written out as an explicit `NO ACTION` by default; when
  omitted, PostgreSQL's implicit `NO ACTION` applies.
- Index `ddl` is now optional.
- The CLI reports Pydantic `ValidationError`s to stderr with a non-zero exit code.
- **JSON Schema generation moved into the docs build**: a MkDocs hook
  (`hooks/json_schema.py`) generates `schema.json` from `ddaml_dict` (instead of `DDL_Dict`)
  on every `mkdocs build`/`serve`, so it is published on each push to `main` and resolves
  in local strict builds. The separate CI generation steps were removed and the download
  link restored.
- Package version set to `2026.10.0a1` (CalVer).
- Examples, the golden output and generated docs updated for the new structure.
- Docstrings cleaned up and code reformatted with `ruff format`; README and CONTRIBUTING
  updated (including the pre-commit workflow).

### Removed

- The unused `tests/samples/examples/` fixtures.
- The "All references resolve!" message printed by `check_references()`.
- `examples/**/output.yaml` is now git-ignored.

### Dependencies

- Updated `pydantic` to 2.14.1, `py-markdown-table` to 2.0.0 (major), `markdown` to 3.11.2,
  `ruff` to 0.17.2 and `ty` to 0.0.92, plus other lock-file updates.
- Added `validators` 0.36.0 (runtime) and `pre-commit` 4.7.0 (dev).
- Updated GitHub Actions (`setup-uv` 10.3.2, `upload-pages-artifact`, `codeql-action`
  4.39.1) via Dependabot.

### Contributors

- Simon Goring


## [2026-09-alpha]

### Added

- **JSON Schema publication**: Auto-generated from Pydantic models and published to docs site
  at `https://ubc-derc.github.io/data_model/schema.json`.
- **Schema documentation page** (`docs/api/schema.md`) with VS Code integration guide for
  editor autocompletion and validation.
- **Pre-commit hook** for `ruff` and `ty` checks on `develop` and `main` branches (gitflow).
- **`ty` type checking** integrated into CI workflow.
- **Dependabot auto-merge workflow** for minor/patch updates with squash merge.
- **Dependabot grouping** for GitHub Actions updates (reduces PR noise).
- `resolve_ref()` utility function to handle `$ref` resolution with sibling key merging.

### Changed

- **Migrated from `ref:` to `$ref:`** for OpenAPI/JSON Schema consistency:
  - Updated `load_database.py`, `load_schema.py`, `load_tables.py` to use `$ref` key.
  - Migrated 90+ YAML files in `examples/` and `tests/samples/`.
  - Updated test fixtures in `test_cli.py` and `test_load_files.py`.
- Redesigned the reference model to align with updated design specifications.
- Updated constraints to use `ConstraintType.FOREIGN_KEY` with `references` block
  (replacing old `REFERENCES` string).
- Improved error messaging for invalid table definitions.
- Generated files (`docs/database/`, `docs/schema.json`) now excluded from version control.
- Refactored test suites for improved coverage of file loading and constraint handling.

### Fixed
- All 62 tests now passing (97.5% coverage) — resolved 6 failures related to `ref`/`$ref`
  migration and constraint type mismatches.

### Dependencies
- Updated `pydantic` to 2.13.5 via Dependabot.
- Updated `ruff` to 0.16.6 via Dependabot.
- Updated `ty` to 0.0.78 via Dependabot.
- Updated `uv-build`, `mkdocs-material`, and GitHub Actions (`deploy-pages`, `setup-uv`,
  `codeql-action`) via Dependabot.

### Contributors
- Simon Goring


## [2026-07-alpha]
### Added
- CLI creates a single YAML from a set of YAML files.
- Documentation with mkdocs.
- YAML schema validation using Pydantic-based classes for key structural elements.
- Test suite.

### Contributors to this Release
* Simon Goring
