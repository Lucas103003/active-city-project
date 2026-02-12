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
│   ├── build_active_index.py
│   └── run_optional_ml_analysis.py
├── src/
│   └── active_city/
│       ├── __init__.py
│       └── index.py
├── tests/
│   └── test_index.py
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

Optional fuer Erweiterung:
- `data/raw/muc_socioeconomic_optional.csv`
  - Vorlage: `data/raw/muc_socioeconomic_optional_template.csv`

## Pipeline

### A) Notebook-basierter Vollprozess
1. `notebooks/00_env_check.ipynb`
2. `notebooks/01_muc_bezirke_und_bevoelkerung.ipynb`
3. `notebooks/02_osm_parks_muc.ipynb`
4. `notebooks/03_osm_sport_muc.ipynb`
5. `notebooks/04_mobility_muc.ipynb`
6. `notebooks/05_active_index_setup.ipynb`

### B) Reproduzierbarer Build aus vorhandenen Zwischenstaenden

```bash
python scripts/build_active_index.py
```

Erzeugt:
- `data/processed/muc_active_city_index.csv`
- `data/processed/muc_active_city_index.geojson`
- `data/processed/muc_active_city_index.gpkg`
- `data/processed/muc_active_city_weight_scenarios.csv`
- `data/processed/muc_active_city_leave_one_out.csv`

### C) Optionale ML-Analyse (PCA + Clustering)

```bash
python scripts/run_optional_ml_analysis.py
```

Erzeugt:
- `data/processed/muc_active_city_ml_typology.csv`
- `data/processed/muc_active_city_ml_summary.txt`

## Tests

```bash
python -m unittest tests/test_index.py
```

Abgedeckt sind u. a.:
- robuste Normalisierung bei konstanten Werten,
- Index-Berechnung,
- Gewichtungsvalidierung,
- Sensitivitaetsausgaben.

## Methodik

Details in:
- `docs/methodik.md`

Kurz:
- Min-Max-Normalisierung,
- Teilindizes: Gruen, Sport, Mobilitaet,
- Gesamtindex mit Baseline-Gewichtung 1/3, 1/3, 1/3,
- Robustheitschecks ueber Gewichtungsszenarien und Leave-one-out.

## Hinweise zur Reproduzierbarkeit

- Notebook-Pfade sind relativ zum `notebooks/`-Ordner (`Path("..")`).
- OSM-basierte Schritte koennen sich ueber die Zeit leicht aendern.
- Das Verzeichnis `notebooks/cache/` enthaelt zwischengespeicherte API-Antworten.
