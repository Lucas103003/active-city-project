# Methodik - Active City Munich

## Ziel
Ein transparenter, reproduzierbarer Bezirksvergleich zu bewegungsrelevanter
Infrastruktur (Gruen, Sport, Mobilitaet) fuer die 25 Stadtbezirke Muenchens.

## Datengrundlage
- Raumbezug: Stadt Muenchen, 25 Stadtbezirke
- Basis: Bezirksgrenzen, Bevoelkerung, Flaeche
- Infrastruktur: Parks, Sportstaetten, OePNV-Haltestellen, Radwege

## Kennzahlen
Pro Bezirk werden genutzt:
- `parks_pro_1000_einw`
- `parks_area_anteil_prozent`
- `sports_pro_1000_einw`
- `sports_area_anteil_prozent`
- `stops_pro_1000_einw`
- `radweg_km_pro_km2`

## Normalisierung
Standardmaessig Min-Max:

`x_norm = (x - min(x)) / (max(x) - min(x))`

Sonderfall: Wenn `max(x) == min(x)`, wird stabil `0.0` vergeben
(Vermeidung Division durch 0).

## Teilindizes
- `index_gruen` = Mittelwert der normalisierten Gruen-Indikatoren
- `index_sport` = Mittelwert der normalisierten Sport-Indikatoren
- `index_mobil` = Mittelwert der normalisierten Mobilitaets-Indikatoren

## Gesamtindex
Baseline:

`active_city_index = (1/3)*index_gruen + (1/3)*index_sport + (1/3)*index_mobil`

## Robustheitschecks
1. Gewichtungsszenarien:
- equal: 0.33 / 0.33 / 0.33
- green_focus: 0.50 / 0.25 / 0.25
- sport_focus: 0.25 / 0.50 / 0.25
- mob_focus: 0.25 / 0.25 / 0.50

Export: `data/processed/muc_active_city_weight_scenarios.csv`

2. Leave-one-out (Indikator entfernen, Rangstabilitaet mit Spearman):

Export: `data/processed/muc_active_city_leave_one_out.csv`

## Optionale Erweiterung (ML)
PCA + Clustering auf den Bezirksprofilen:
- Script: `scripts/run_optional_ml_analysis.py`
- Exporte:
  - `data/processed/muc_active_city_ml_typology.csv`
  - `data/processed/muc_active_city_ml_summary.txt`

## Optionale soziooekonomische Merkmale
Falls verfuegbar, koennen z. B. Altersstruktur oder Einkommen pro Bezirk
hinzugefuegt werden. Ein Template liegt hier:

`data/raw/muc_socioeconomic_optional_template.csv`
