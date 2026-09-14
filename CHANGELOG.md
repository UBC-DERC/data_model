# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) using a YYYY-MM model.

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