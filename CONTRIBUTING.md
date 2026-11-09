# Contributing to `data_model`

We want to make contributing to this project as easy and transparent as possible. We also want to support broader community adoption of this tool, and transparent adoption of the data standards.

## Coding Practice

This project uses `uv` as a package manager and to manage virtual environments. To use development tools including `ruff` and `ty`, you first need to install and synchronize the project. First check that you have [`uv` installed](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
```

We use a `ruff` and `ty` pre-commit hook (see [`.pre-commit-config.yaml`](.pre-commit-config.yaml)) to ensure code quality and standardization. To enable this hook when you are developing code, use the following commands:

```bash
uv run pre-commit install
uv run pre-commit run --all-files   # one-time pass over the existing code
```

The `pre-commit` hook will run both `ruff` and `ty`.

## Pull Requests

We actively welcome your pull requests.

### For new validation or class structures

1. Create a GitHub issue proposing a change to a class definition within the data model (you can stop here if you'd like).
2. Fork the repo and create your branch from `main`.
3. Modify the code as needed and add new tests to ensure your code runs as expected.
4. If you've added an example, it should be validated. You can do this by running:
     `data-model ./examples/... -o new_test.yaml --docs ./docs`
     (once you've followed the installation guidelines).
5. Verify that there are no issues in your doc build. You can check the preview locally by entering your virtual environment and running `mkdocs serve`.
6. *Make sure that you are testing against an updated data model*
   * Run `pytest` with the `UPDATE_GOLDEN=1` environment variable: `UPDATE_GOLDEN=1 uv run pytest`.
7. Address any feedback in code review promptly.

## For bug fixes

1. Create a GitHub issue identifying a bug (you can stop here if you'd like).
2. Fork the repo and create your branch from `main`.
3. Install `uv` and run `uv sync`
4. Make your code change and ensure `ruff`, `ty` and `pytest` checks run cleanly.
5. Address any feedback in code review promptly.

## For "Best Practices" Documentation

1. Create a GitHub issue identifying a documentation deficiency (you can stop here if you'd like).
2. Fork the repo and create your branch from `main`.
3. Install `uv` and run `uv sync`
4. Edit documentation in the `docs` and check that it is showing up properly by running `uv run mkdocs serve`.
5. Address any feedback in code review promptly.

## Issues

We use [GitHub issues](https://github.com/UBC-DERC/data_model) to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

## License

By contributing to this project's code, documentation and examples you agree that your contributions will be licensed under the [LICENSE file](LICENSE.md) in the root directory of this source tree.
