# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) using a YYYY-MM model.

## [2026-09-alpha]

### Added
- Implementation of `$ref` support for better consistency with OpenAPI standards.
- New `resolve_ref` utility function to handle internal reference resolution.
- Enhanced constraint and index capabilities, allowing for the inclusion or exclusion of specific
keys (e.g., `database`, `schema`, `table`, `column`).

### Changed
- Redesigned the reference model to align with updated design specifications.
- Updated constraints, indexes, and references to accommodate new key structures.
- Improved error messaging for invalid table definitions to provide clearer feedback on structural
errors.
- Refactored test suites for improved coverage of file loading (`load_files`) and primary key
references.
- Updated project documentation to reflect the updated shapes of constraints and references.

### Dependencies
- Updated `pydantic` (to 2.13.5) via Dependabot.
- Updated `ruff` (to 0.16.6) via Dependabot.
- Updated `uv`, `mkdocs-material`, and GitHub Actions (`deploy-pages`) via Dependabot.


## [2026-07-alpha]
### Added
- CLI creates a single YAML from a set of YAML files.
- Documentation with mkdocs.
- YAML schema validation using Pydantic-based classes for key structural elements.
- Test suite.

### Contributors to this Release
* Simon Goring