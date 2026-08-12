"""Command-line entry point.

Validate a YAML data model and, only if it is valid, write the composite YAML
artifact and the documentation. Validation failures are reported verbosely (all
problems at once) to stderr and cause a non-zero exit code with no output
written, so the tool can gate a deployment pipeline.
"""
import argparse
import sys
from pathlib import Path

import yaml

from .check_references import ReferenceCheckError
from .createDocs import document_database
from .load_database import load_database
from .model_build import ModelValidationError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="data-model",
        description="Validate a YAML data model and write documentation and a composite YAML file.",
    )
    parser.add_argument("entry", help="Path to the database entry YAML file.")
    parser.add_argument("--docs", required=True, help="Output directory for documentation.")
    parser.add_argument("-o", "--output", required=True, help="Path for the composite output YAML.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI. Returns the process exit code (0 success, 1 on validation failure)."""
    args = _build_parser().parse_args(argv)

    try:
        database = load_database(args.entry)
    except (ModelValidationError, ReferenceCheckError) as error:
        print(error, file=sys.stderr)
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as handle:
        yaml.safe_dump(database.model_dump(by_alias=True), handle)
    document_database(database, args.docs)
    print(f"Wrote {args.output} and documentation to {args.docs}")
    return 0
