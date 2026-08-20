# Contributing to `data_model``

We want to make contributing to this project as easy and transparent as
possible. We also want to support broader community adoption of this tool, and transparent adoption of the data standards.

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
6. Address any feedback in code review promptly.

## For bug fixes

1. Fork the repo and create your branch from `main`.
3. Install `uv` and run `uv sync`
4. Make your code change and ensure `ruff`, `ty` and `pytest` checks run cleanly.
5. Address any feedback in code review promptly.

## Issues

We use [GitHub issues](https://github.com/UBC-DERC/data_model) to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

## License

By contributing to examples, you agree that your contributions will be licensed
under the [LICENSE file](LICENSE.md) in the root directory of this source tree.
