#!/usr/bin/env python3
"""Set execution_count to null for code cells in Jupyter notebooks.

By default, scans the ./notebooks directory recursively.
Does not modify outputs or markdown content.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def iter_notebooks(paths: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_file() and p.suffix == ".ipynb":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.ipynb")))
    return sorted(set(files))


def clean_execution_counts(nb_path: Path) -> tuple[bool, int]:
    data = json.loads(nb_path.read_text(encoding="utf-8"))
    changed = 0

    for cell in data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            changed += 1

    if changed:
        nb_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )

    return (changed > 0, changed)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set execution_count to null in .ipynb files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["notebooks"],
        help="Files or directories to scan (default: notebooks)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if changes are needed; do not write files.",
    )
    args = parser.parse_args()

    targets = iter_notebooks([Path(p) for p in args.paths])
    if not targets:
        print("No notebooks found.")
        return 0

    changed_files = 0
    changed_cells_total = 0

    if args.check:
        for nb in targets:
            data = json.loads(nb.read_text(encoding="utf-8"))
            dirty_cells = sum(
                1
                for cell in data.get("cells", [])
                if cell.get("cell_type") == "code"
                and cell.get("execution_count") is not None
            )
            if dirty_cells:
                changed_files += 1
                changed_cells_total += dirty_cells
                print(f"needs-clean: {nb} ({dirty_cells} cells)")

        if changed_files:
            print(
                f"Execution counts need cleaning in {changed_files} notebooks "
                f"({changed_cells_total} cells)."
            )
            return 1

        print("All notebooks already clean.")
        return 0

    for nb in targets:
        file_changed, changed_cells = clean_execution_counts(nb)
        if file_changed:
            changed_files += 1
            changed_cells_total += changed_cells
            print(f"cleaned: {nb} ({changed_cells} cells)")

    print(
        f"Done. Cleaned {changed_files} notebooks "
        f"({changed_cells_total} cells set to null)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
