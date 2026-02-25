# Methodik - Active City Munich

## Ziel
Ein transparenter Bezirksvergleich zu bewegungsrelevanter Infrastruktur
(Gruen, Sport, Mobilitaet) fuer die 25 Stadtbezirke Muenchens.

## Datengrundlage
- Raumbezug: Stadt Muenchen, 25 Stadtbezirke
- Basis: Bezirksgrenzen, Bevoelkerung, Flaeche
- Infrastruktur: Parks, Sportstaetten, OePNV-Haltestellen, Radwege

## Datenstand und Abrufzeitpunkt
- Bevoelkerungsdaten: **Stand 31.12.2024**.
- Administrative Geodaten und Bevoelkerungsdaten stammen aus den in `data/raw/`
  abgelegten Projektquellen.
- OSM-basierte Layer (Parks, Sport, Mobilitaet) werden zum Ausfuehrungszeitpunkt
  ueber OSMnx abgefragt und anschliessend als Zwischen-/Ergebnisdaten gespeichert.
- Fuer die Vergleichbarkeit im Bericht sollte der Abrufzeitpunkt (Datum/Uhrzeit)
  dokumentiert werden, da sich OSM-Daten laufend aendern koennen.

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

## OSM-Limitierungen und potenzielle Verzerrungen
- OSM ist ein Community-Datensatz; Vollstaendigkeit und Attributqualitaet koennen
  je Bezirk unterschiedlich sein.
- Unterschiede in der lokalen Mapping-Aktivitaet koennen als scheinbare
  Infrastrukturunterschiede im Index erscheinen.
- Tagging ist nicht immer einheitlich (z. B. `access`, `fee`, `cycleway`), was
  insbesondere qualitative Proxy-Indikatoren beeinflussen kann.

## Umgang mit Nullwerten
- Nach dem Merge werden fehlende Kennzahlwerte in den Kernindikatoren als `0`
  gesetzt, um vollstaendige Bezirksvergleiche und stabile Berechnungen zu
  ermoeglichen.
- Interpretation: `0` bedeutet hier "kein nachweisbarer Treffer in den
  verwendeten Quelldaten", nicht zwingend "real nicht vorhanden".
- Diese Annahme sollte bei Ergebnisinterpretation und Handlungsempfehlungen
  explizit genannt werden.

## Robustheitsidee
Im Notebook 05 werden zusaetzliche Gewichtungsszenarien und Rangvergleiche
explorativ geprueft (z. B. Green-/Sport-/Mobility-Fokus).

## Sensitivitaet der Gewichtung
- Die Baseline nutzt gleiche Gewichte der drei Domaenen (Gruen/Sport/Mobilitaet).
- In Notebook 05 werden alternative Gewichtungen und Rangverschiebungen berechnet,
  um die Robustheit gegen normative Gewichtungsentscheidungen zu pruefen.
- Fuer den Bericht sollten neben Baseline-Rankings immer auch diese
  Sensitivitaetsbefunde (z. B. Spearman-Korrelationen, Rangdeltas) ausgewiesen
  werden.

## Optionale Erweiterung
- weitere soziooekonomische Bezirkseigenschaften
- Typisierung ueber PCA/Clusterverfahren
- Qualitaetsindikatoren:
  - Parkzugaenglichkeit (Public/Fee-Proxy)
  - Sportanlagen-Typendiversitaet und Oeffentlichkeit
  - Radweg-Sicherheit (Anteil geschuetzter Radinfrastruktur)
