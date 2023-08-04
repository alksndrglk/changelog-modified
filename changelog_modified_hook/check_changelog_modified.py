from __future__ import annotations

import argparse
from typing import Sequence


def find_changelog_in_added_files(
    filenames: Sequence[str],
    *,
    changelog_name: str = "CHANGELOG.md",
) -> bool:
    filenames_filtered = set(filenames)
    return changelog_name in filenames_filtered


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--changelog-name",
        help="Name of Changelog in project.",
        default="CHANGELOG.md",
    )
    args = parser.parse_args(argv)

    return find_changelog_in_added_files(
        args.filenames,
        changelog_name=args.changelog_name,
    )


if __name__ == "__main__":
    raise SystemExit(main())
