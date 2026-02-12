"""Index calculation utilities for Munich Active City analysis."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

DEFAULT_INDICATORS: Dict[str, list[str]] = {
    "green": ["parks_pro_1000_einw", "parks_area_anteil_prozent"],
    "sport": ["sports_pro_1000_einw", "sports_area_anteil_prozent"],
    "mob": ["stops_pro_1000_einw", "radweg_km_pro_km2"],
}

DEFAULT_WEIGHTS: Dict[str, float] = {"green": 1 / 3, "sport": 1 / 3, "mob": 1 / 3}


def normalize_series(series: pd.Series, method: str = "minmax") -> pd.Series:
    """Normalize a numeric series with stable handling for constant values."""
    x = pd.to_numeric(series, errors="coerce")

    if method == "minmax":
        min_val = x.min(skipna=True)
        max_val = x.max(skipna=True)
        denom = max_val - min_val
        if pd.isna(denom) or np.isclose(denom, 0):
            return pd.Series(0.0, index=series.index)
        return (x - min_val) / denom

    if method == "zscore":
        mean_val = x.mean(skipna=True)
        std_val = x.std(skipna=True)
        if pd.isna(std_val) or np.isclose(std_val, 0):
            return pd.Series(0.0, index=series.index)
        return (x - mean_val) / std_val

    raise ValueError(f"Unknown method: {method}")


def _validate_weights(weights: Mapping[str, float]) -> None:
    required_keys = {"green", "sport", "mob"}
    missing = required_keys.difference(weights)
    if missing:
        raise ValueError(f"Missing weight keys: {sorted(missing)}")

    total = float(weights["green"] + weights["sport"] + weights["mob"])
    if not np.isclose(total, 1.0, atol=1e-6):
        raise ValueError(f"Weights must sum to 1.0, got {total:.6f}")


def _all_indicator_columns(indicators: Mapping[str, Iterable[str]]) -> list[str]:
    all_cols: list[str] = []
    for key in ("green", "sport", "mob"):
        all_cols.extend(list(indicators[key]))
    return sorted(set(all_cols))


def compute_active_city_index(
    df: pd.DataFrame,
    indicators: Mapping[str, Iterable[str]] | None = None,
    weights: Mapping[str, float] | None = None,
    norm_method: str = "minmax",
    fillna_value: float = 0.0,
    copy: bool = True,
) -> pd.DataFrame:
    """Compute sub-indices and Active City Index on district-level data."""
    indicators = indicators or DEFAULT_INDICATORS
    weights = weights or DEFAULT_WEIGHTS
    _validate_weights(weights)

    gdf = df.copy() if copy else df

    for col in _all_indicator_columns(indicators):
        if col not in gdf.columns:
            raise KeyError(f"Indicator column missing: {col}")
        gdf[col] = pd.to_numeric(gdf[col], errors="coerce").fillna(fillna_value)
        gdf[f"{col}_norm"] = normalize_series(gdf[col], method=norm_method)

    gdf["index_gruen"] = gdf[[f"{c}_norm" for c in indicators["green"]]].mean(axis=1)
    gdf["index_sport"] = gdf[[f"{c}_norm" for c in indicators["sport"]]].mean(axis=1)
    gdf["index_mobil"] = gdf[[f"{c}_norm" for c in indicators["mob"]]].mean(axis=1)

    gdf["active_city_index"] = (
        float(weights["green"]) * gdf["index_gruen"]
        + float(weights["sport"]) * gdf["index_sport"]
        + float(weights["mob"]) * gdf["index_mobil"]
    )

    return gdf


def compute_weight_sensitivity(
    indexed_df: pd.DataFrame,
    scenarios: Mapping[str, Mapping[str, float]] | None = None,
) -> pd.DataFrame:
    """Create rank comparison table for different weighting scenarios."""
    if scenarios is None:
        scenarios = {
            "equal": {"green": 1 / 3, "sport": 1 / 3, "mob": 1 / 3},
            "green_focus": {"green": 0.5, "sport": 0.25, "mob": 0.25},
            "sport_focus": {"green": 0.25, "sport": 0.5, "mob": 0.25},
            "mob_focus": {"green": 0.25, "sport": 0.25, "mob": 0.5},
        }

    base = indexed_df.copy()

    for scenario, weights in scenarios.items():
        _validate_weights(weights)
        score_col = f"aci_{scenario}"
        base[score_col] = (
            float(weights["green"]) * base["index_gruen"]
            + float(weights["sport"]) * base["index_sport"]
            + float(weights["mob"]) * base["index_mobil"]
        )
        rank_col = f"rank_{scenario}"
        base[rank_col] = (
            base[score_col].rank(method="min", ascending=False).astype(int)
        )

    base["delta_rank_green_focus_vs_equal"] = (
        base["rank_green_focus"] - base["rank_equal"]
    )
    base["delta_rank_sport_focus_vs_equal"] = (
        base["rank_sport_focus"] - base["rank_equal"]
    )
    base["delta_rank_mob_focus_vs_equal"] = (
        base["rank_mob_focus"] - base["rank_equal"]
    )

    keep_cols = [
        "bez_nr",
        "name",
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
    return base[keep_cols].sort_values("rank_equal")


def compute_leave_one_out_sensitivity(
    source_df: pd.DataFrame,
    indicators: Mapping[str, Iterable[str]] | None = None,
) -> pd.DataFrame:
    """Compute Spearman rank stability when removing one indicator at a time."""
    indicators = indicators or DEFAULT_INDICATORS

    base = compute_active_city_index(source_df, indicators=indicators, copy=True)
    base_scores = base[["bez_nr", "active_city_index"]].rename(
        columns={"active_city_index": "aci_base"}
    )

    rows: list[dict[str, object]] = []

    for dim in ("green", "sport", "mob"):
        for removed in indicators[dim]:
            new_indicators = {
                "green": list(indicators["green"]),
                "sport": list(indicators["sport"]),
                "mob": list(indicators["mob"]),
            }
            new_indicators[dim] = [x for x in new_indicators[dim] if x != removed]

            tmp = compute_active_city_index(source_df, indicators=new_indicators, copy=True)
            merged = base_scores.merge(
                tmp[["bez_nr", "active_city_index"]].rename(
                    columns={"active_city_index": "aci_loo"}
                ),
                on="bez_nr",
                how="inner",
            )
            rho, p_value = spearmanr(merged["aci_base"], merged["aci_loo"])
            rows.append(
                {
                    "dimension": dim,
                    "removed_indicator": removed,
                    "spearman_rho": float(rho),
                    "p_value": float(p_value),
                }
            )

    return pd.DataFrame(rows).sort_values("spearman_rho", ascending=False)
