#!/usr/bin/env python3
"""Build Active City outputs from interim/processed district indicator datasets."""

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from active_city.index import (  # noqa: E402
    DEFAULT_INDICATORS,
    compute_active_city_index,
    compute_leave_one_out_sensitivity,
    compute_weight_sensitivity,
)

INTERIM_DIR = ROOT / "data" / "interim"
PROCESSED_DIR = ROOT / "data" / "processed"


def _load_base() -> gpd.GeoDataFrame:
    gdf_base = gpd.read_file(INTERIM_DIR / "muc_bezirke_bev_clean.geojson")

    gdf_parks = gpd.read_file(PROCESSED_DIR / "muc_bezirke_parks.geojson")[[
        "bez_nr",
        "parks_pro_1000_einw",
        "parks_area_anteil_prozent",
    ]]
    gdf_sport = gpd.read_file(PROCESSED_DIR / "muc_bezirke_sport.geojson")[[
        "bez_nr",
        "sports_pro_1000_einw",
        "sports_area_anteil_prozent",
    ]]
    gdf_mob = gpd.read_file(PROCESSED_DIR / "muc_bezirke_mobility.geojson")[[
        "bez_nr",
        "stops_pro_1000_einw",
        "radweg_km_pro_km2",
    ]]

    return (
        gdf_base.merge(gdf_parks, on="bez_nr", how="left")
        .merge(gdf_sport, on="bez_nr", how="left")
        .merge(gdf_mob, on="bez_nr", how="left")
    )


def build_outputs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    base = _load_base()
    indexed = compute_active_city_index(base, indicators=DEFAULT_INDICATORS)

    weight_table = compute_weight_sensitivity(indexed)
    indexed = indexed.merge(weight_table, on=["bez_nr", "name"], how="left")
    loo_table = compute_leave_one_out_sensitivity(base, indicators=DEFAULT_INDICATORS)

    export_cols = [
        "bez_nr",
        "name",
        "einwohner",
        "flaeche_ha",
        "einwohnerdichte",
        "parks_pro_1000_einw",
        "parks_area_anteil_prozent",
        "sports_pro_1000_einw",
        "sports_area_anteil_prozent",
        "stops_pro_1000_einw",
        "radweg_km_pro_km2",
        "index_gruen",
        "index_sport",
        "index_mobil",
        "active_city_index",
        "aci_equal",
        "aci_green_focus",
        "aci_sport_focus",
        "aci_mob_focus",
        "rank_equal",
        "rank_green_focus",
        "rank_sport_focus",
        "rank_mob_focus",
        "delta_rank_green_focus_vs_equal",
        "delta_rank_sport_focus_vs_equal",
        "delta_rank_mob_focus_vs_equal",
    ]

    out_csv = PROCESSED_DIR / "muc_active_city_index.csv"
    indexed[export_cols].to_csv(out_csv, index=False, float_format="%.6f")

    out_geojson = PROCESSED_DIR / "muc_active_city_index.geojson"
    indexed[export_cols + ["geometry"]].to_file(out_geojson, driver="GeoJSON")

    out_gpkg = PROCESSED_DIR / "muc_active_city_index.gpkg"
    indexed[export_cols + ["geometry"]].to_file(
        out_gpkg, layer="muc_active_index", driver="GPKG"
    )

    out_weight = PROCESSED_DIR / "muc_active_city_weight_scenarios.csv"
    weight_table.to_csv(out_weight, index=False, float_format="%.6f")

    out_loo = PROCESSED_DIR / "muc_active_city_leave_one_out.csv"
    loo_table.to_csv(out_loo, index=False, float_format="%.6f")

    print(f"Wrote: {out_csv}")
    print(f"Wrote: {out_geojson}")
    print(f"Wrote: {out_gpkg}")
    print(f"Wrote: {out_weight}")
    print(f"Wrote: {out_loo}")


if __name__ == "__main__":
    build_outputs()
