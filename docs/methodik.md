# Methodik - Active City Munich

## Ziel
Ein transparenter Bezirksvergleich zu bewegungsrelevanter Infrastruktur
(Gruen, Sport, Mobilitaet) fuer die 25 Stadtbezirke Muenchens.

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
Min-Max-Standardisierung:

`x_norm = (x - min(x)) / (max(x) - min(x))`

Hinweis: Bei konstanten Reihen muss der Sonderfall `max(x) == min(x)` sauber
behandelt werden, um Division durch 0 zu vermeiden.

## Teilindizes
- `index_gruen` = Mittelwert der normalisierten Gruen-Indikatoren
- `index_sport` = Mittelwert der normalisierten Sport-Indikatoren
- `index_mobil` = Mittelwert der normalisierten Mobilitaets-Indikatoren

## Gesamtindex
Baseline:

`active_city_index = (1/3)*index_gruen + (1/3)*index_sport + (1/3)*index_mobil`

## Robustheitsidee
Im Notebook 05 werden zusaetzliche Gewichtungsszenarien und Rangvergleiche
explorativ geprueft (z. B. Green-/Sport-/Mobility-Fokus).

## Optionale Erweiterung
- weitere soziooekonomische Bezirkseigenschaften
- Typisierung ueber PCA/Clusterverfahren
- Qualitaetsindikatoren:
  - Parkzugaenglichkeit (Public/Fee-Proxy)
  - Sportanlagen-Typendiversitaet und Oeffentlichkeit
  - Radweg-Sicherheit (Anteil geschuetzter Radinfrastruktur)
