# Active City Project (Munich)

Dieses Projekt erstellt einen **Active City Index** fuer die 25 Muenchner Stadtbezirke.
Die Analyse kombiniert Gruenflaechen-, Sport- und Mobilitaetsindikatoren auf Basis von
Geo- und OSM-Daten und erzeugt reproduzierbare Ergebnisse fuer Bericht und Karten.

## Zielbild

- Vergleichbare Kennzahlen auf Bezirksebene erzeugen
- Einen transparenten, gewichtbaren Gesamtindex berechnen
- Ergebnisartefakte fuer Paper/Report exportieren (Tabellen, Karten, Geodaten)

## Projektstruktur

```text
active-city-project/
├── data/
│   ├── raw/                 # Eingangsdaten (GeoJSON, CSV)
│   ├── interim/             # Zwischenergebnisse
│   └── processed/           # Finale Index- und Indikator-Daten
├── docs/
│   ├── methodik.md
│   ├── index_overview.html
├── notebooks/               # 00 bis 05 Analyse-Workflow
├── outputs/
│   ├── figures/             # Exportierte Abbildungen je Notebook
│   └── tables/              # Exportierte Tabellen je Notebook
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

Pflichtdaten in `data/raw/`:
- `muc_stadtbezirke.geojson`
- `bev_stadtbezirke.csv`



## Pipeline (Notebook-First)

Die Notebooks in dieser Reihenfolge ausfuehren:

1. `notebooks/00_env_check.ipynb`
2. `notebooks/01_muc_bezirke_und_bevoelkerung.ipynb`
3. `notebooks/02_osm_parks_muc.ipynb`
4. `notebooks/03_osm_sport_muc.ipynb`
5. `notebooks/04_mobility_muc.ipynb`
6. `notebooks/05_active_index_setup.ipynb`

Empfehlung: Pro Notebook `Restart & Run All` verwenden.

## Inhalte je Notebook (kurz)

- `00_env_check`: Environment- und Datenbasis-Checks
- `01_muc_bezirke_und_bevoelkerung`: Bezirksbasis, Bevoelkerung, Flaeche, Dichte
- `02_osm_parks_muc`: Park-Indikatoren pro Bezirk
- `03_osm_sport_muc`: Sport-Indikatoren pro Bezirk
- `04_mobility_muc`: OePNV- und Radwege-Indikatoren
- `05_active_index_setup`: Normalisierung, Gewichtung, Index, Sensitivitaet, Exporte

## Wichtigste Outputs

Finale Daten (`data/processed/`):
- `muc_active_city_index.csv`
- `muc_active_city_index.geojson`
- `muc_active_city_index.gpkg`
- `muc_active_city_quality_index.csv`
- `muc_bezirke_parks.geojson`
- `muc_bezirke_sport.geojson`
- `muc_bezirke_mobility.geojson`

Berichtsartefakte (`outputs/`):
- `outputs/figures/01_bezirke_bevoelkerung/`
- `outputs/figures/02_parks/`
- `outputs/figures/03_sport/`
- `outputs/figures/04_mobility/`
- `outputs/figures/05_active_index/`
- `outputs/tables/...` analog je Notebook

## Notebook-Cleanup (fuer saubere Commits)

```bash
python scripts/clean_notebooks.py
```

Wirkung:
- setzt `execution_count` auf `null`
- entfernt Output-Objekte
- reduziert Notebook-Diffs in Git

## Methodik und Dokumentation

- Methodik: `docs/methodik.md`
- Interaktive Index-Uebersicht: `docs/index_overview.html`

## Reproduzierbarkeit / Hinweise

- Notebook-Pfade sind relativ zum `notebooks/`-Ordner (`Path("..")`).
- OSM-basierte Ergebnisse koennen sich zeitlich leicht aendern.
