"""Local convenience wrapper around the packaged CLI.

Prefer the installed console script: ``data-model <entry.yaml> --docs <dir> --output <file>``.
"""
import sys

from data_model.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
