# Active City Project (Munich)

Dieses Projekt erstellt einen **Active City Index** fuer die 25 Muenchner
Stadtbezirke auf Basis von Gruen-, Sport- und Mobilitaetsindikatoren.

## Projektstruktur

```text
active-city-project/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── docs/
│   └── methodik.md
├── notebooks/
├── scripts/
│   └── clean_notebooks.py
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Eingabedaten

Pflichtdaten:
- `data/raw/muc_stadtbezirke.geojson`
- `data/raw/bev_stadtbezirke.csv`

## Pipeline (Notebook-First)

Fuehre die Notebooks in dieser Reihenfolge aus:

1. `notebooks/00_env_check.ipynb`
2. `notebooks/01_muc_bezirke_und_bevoelkerung.ipynb`
3. `notebooks/02_osm_parks_muc.ipynb`
4. `notebooks/03_osm_sport_muc.ipynb`
5. `notebooks/04_mobility_muc.ipynb`
6. `notebooks/05_active_index_setup.ipynb`

## Wichtigste Outputs

Nach erfolgreichem Lauf:
- `data/processed/muc_active_city_index.csv`
- `data/processed/muc_active_city_index.geojson`
- `data/processed/muc_active_city_index.gpkg`

## Notebook-Cleanup (optional)

```bash
python scripts/clean_notebooks.py
```

Wirkung:
- einheitliche Intro-Struktur je Notebook,
- bereinigte Zell-Metadaten,
- Outputs und Execution-Counts entfernt (saubere Commits).

## Methodik

Details in:
- `docs/methodik.md`

## Hinweise zur Reproduzierbarkeit

- Notebook-Pfade sind relativ zum `notebooks/`-Ordner (`Path("..")`).
- OSM-basierte Schritte koennen sich ueber die Zeit leicht aendern.
- `notebooks/cache/` enthaelt zwischengespeicherte API-Antworten.
