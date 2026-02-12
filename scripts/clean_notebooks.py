#!/usr/bin/env python3
"""Standardize project notebooks to a clean, reproducible structure."""

from __future__ import annotations

from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"

NB_INFO = {
    "00_env_check.ipynb": {
        "title": "00 - Environment Check",
        "goal": "Prueft Python- und Geospatial-Abhaengigkeiten fuer den Projektlauf.",
        "inputs": "Keine Projektdateien erforderlich.",
        "outputs": "Sichtpruefung der installierten Paketversionen.",
    },
    "01_muc_bezirke_und_bevoelkerung.ipynb": {
        "title": "01 - Bezirke und Bevoelkerung",
        "goal": "Bereitet Bezirksgrenzen und Bevoelkerungsdaten als Basisdatensatz auf.",
        "inputs": "data/raw/muc_stadtbezirke.geojson, data/raw/bev_stadtbezirke.csv",
        "outputs": "data/interim/muc_bezirke_bev_clean.geojson",
    },
    "02_osm_parks_muc.ipynb": {
        "title": "02 - Parks pro Bezirk",
        "goal": "Ermittelt Parkindikatoren pro Stadtbezirk auf OSM-Basis.",
        "inputs": "data/interim/muc_bezirke_bev_clean.geojson, OSM-Parks",
        "outputs": "data/processed/muc_bezirke_parks.geojson",
    },
    "03_osm_sport_muc.ipynb": {
        "title": "03 - Sportstaetten pro Bezirk",
        "goal": "Ermittelt Sportinfrastruktur-Indikatoren pro Stadtbezirk auf OSM-Basis.",
        "inputs": "data/interim/muc_bezirke_bev_clean.geojson, OSM-Sportstaetten",
        "outputs": "data/processed/muc_bezirke_sport.geojson",
    },
    "04_mobility_muc.ipynb": {
        "title": "04 - Mobilitaet pro Bezirk",
        "goal": "Ermittelt OePNV- und Radwegeindikatoren pro Stadtbezirk auf OSM-Basis.",
        "inputs": "data/interim/muc_bezirke_bev_clean.geojson, OSM-Haltestellen, OSM-Radwege",
        "outputs": "data/processed/muc_bezirke_mobility.geojson",
    },
    "05_active_index_setup.ipynb": {
        "title": "05 - Active City Index",
        "goal": "Fuehrt alle Teilindikatoren zusammen und berechnet den Active City Index.",
        "inputs": "interim + processed Indikator-Dateien aus 01-04",
        "outputs": "data/processed/muc_active_city_index.(csv|geojson|gpkg)",
    },
}


def make_intro(filename: str) -> nbformat.NotebookNode:
    meta = NB_INFO.get(filename)
    if not meta:
        title = filename.replace(".ipynb", "")
        goal = "Notebook im Active-City-Workflow."
        inputs = "Siehe Notebook-Code"
        outputs = "Siehe Notebook-Code"
    else:
        title = meta["title"]
        goal = meta["goal"]
        inputs = meta["inputs"]
        outputs = meta["outputs"]

    text = (
        f"# {title}\n\n"
        "## Ziel\n"
        f"{goal}\n\n"
        "## Inputs\n"
        f"- {inputs}\n\n"
        "## Outputs\n"
        f"- {outputs}\n\n"
        "## Ausfuehrung\n"
        "- Von oben nach unten ausfuehren (Restart & Run All).\n"
        "- Dieses Notebook ist Teil der Pipeline 00 -> 05.\n"
    )
    return nbformat.v4.new_markdown_cell(text)


def clean_notebook(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)

    # Normalize top-level metadata for consistency
    nb.metadata.setdefault("kernelspec", {})
    nb.metadata["kernelspec"]["name"] = "python3"
    nb.metadata["kernelspec"]["display_name"] = ".venv"
    nb.metadata["kernelspec"]["language"] = "python"
    nb.metadata.setdefault("language_info", {})
    nb.metadata["language_info"]["name"] = "python"

    intro = make_intro(path.name)

    cells = nb.cells
    if cells and cells[0].get("cell_type") == "markdown" and "## Ziel" in "".join(cells[0].get("source", [])):
        cells[0] = intro
    else:
        cells = [intro] + cells

    for cell in cells:
        # keep notebook lean and review-friendly
        cell["metadata"] = {}
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    nb.cells = cells
    nbformat.write(nb, path)


def main() -> None:
    notebooks = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    for nb_path in notebooks:
        clean_notebook(nb_path)
        print(f"Cleaned: {nb_path}")


if __name__ == "__main__":
    main()
