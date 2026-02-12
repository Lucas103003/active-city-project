#!/usr/bin/env python3
"""Optional PCA + clustering on Active City index outputs."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

PROCESSED_DIR = ROOT / "data" / "processed"


def run_optional_ml() -> None:
    source_csv = PROCESSED_DIR / "muc_active_city_index.csv"
    if not source_csv.exists():
        raise FileNotFoundError(
            "Missing processed index file. Run scripts/build_active_index.py first."
        )

    df = pd.read_csv(source_csv)

    features = [
        "index_gruen",
        "index_sport",
        "index_mobil",
        "parks_pro_1000_einw",
        "sports_pro_1000_einw",
        "stops_pro_1000_einw",
        "radweg_km_pro_km2",
    ]

    socio_path = ROOT / "data" / "raw" / "muc_socioeconomic_optional.csv"
    if socio_path.exists():
        socio = pd.read_csv(socio_path)
        if "bez_nr" in socio.columns:
            df = df.merge(socio, on="bez_nr", how="left")
            optional_cols = [
                col for col in socio.columns if col != "bez_nr" and col in df.columns
            ]
            features.extend(optional_cols)

    features = list(dict.fromkeys(features))
    X = df[features].copy()
    X = X.fillna(0.0)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(Xs)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=20)
    clusters = kmeans.fit_predict(Xs)

    result = df[["bez_nr", "name", "active_city_index"]].copy()
    result["pca_1"] = pcs[:, 0]
    result["pca_2"] = pcs[:, 1]
    result["cluster_k4"] = clusters

    out_detail = PROCESSED_DIR / "muc_active_city_ml_typology.csv"
    result.to_csv(out_detail, index=False, float_format="%.6f")

    explained = pca.explained_variance_ratio_
    out_summary = PROCESSED_DIR / "muc_active_city_ml_summary.txt"
    with out_summary.open("w", encoding="utf-8") as f:
        f.write("PCA explained variance ratio\n")
        f.write(f"PC1: {explained[0]:.6f}\n")
        f.write(f"PC2: {explained[1]:.6f}\n")
        f.write(f"Cumulative: {(explained[0] + explained[1]):.6f}\n\n")
        f.write("Cluster sizes (k=4)\n")
        counts = result["cluster_k4"].value_counts().sort_index()
        for cluster_id, cnt in counts.items():
            f.write(f"cluster_{cluster_id}: {cnt}\n")

    print(f"Wrote: {out_detail}")
    print(f"Wrote: {out_summary}")


if __name__ == "__main__":
    run_optional_ml()
