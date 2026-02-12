import unittest

import pandas as pd

from src.active_city.index import (
    DEFAULT_INDICATORS,
    compute_active_city_index,
    compute_leave_one_out_sensitivity,
    compute_weight_sensitivity,
    normalize_series,
)


class TestIndexFunctions(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "bez_nr": [1, 2, 3],
                "name": ["A", "B", "C"],
                "parks_pro_1000_einw": [1.0, 2.0, 3.0],
                "parks_area_anteil_prozent": [5.0, 5.0, 5.0],
                "sports_pro_1000_einw": [0.1, 0.3, 0.2],
                "sports_area_anteil_prozent": [1.0, 2.0, 3.0],
                "stops_pro_1000_einw": [10.0, 20.0, 30.0],
                "radweg_km_pro_km2": [0.5, 0.8, 0.6],
            }
        )

    def test_normalize_constant_series(self):
        s = pd.Series([7.0, 7.0, 7.0])
        out = normalize_series(s, method="minmax")
        self.assertTrue((out == 0.0).all())

    def test_compute_index_creates_required_columns(self):
        out = compute_active_city_index(self.df)
        required = ["index_gruen", "index_sport", "index_mobil", "active_city_index"]
        for col in required:
            self.assertIn(col, out.columns)
            self.assertFalse(out[col].isna().any())

    def test_weights_must_sum_to_one(self):
        with self.assertRaises(ValueError):
            compute_active_city_index(
                self.df,
                weights={"green": 0.5, "sport": 0.5, "mob": 0.5},
            )

    def test_weight_sensitivity_shape(self):
        indexed = compute_active_city_index(self.df)
        table = compute_weight_sensitivity(indexed)
        self.assertEqual(len(table), len(self.df))
        self.assertIn("delta_rank_mob_focus_vs_equal", table.columns)

    def test_leave_one_out_contains_all_indicators(self):
        table = compute_leave_one_out_sensitivity(self.df, indicators=DEFAULT_INDICATORS)
        expected_rows = sum(len(v) for v in DEFAULT_INDICATORS.values())
        self.assertEqual(len(table), expected_rows)
        self.assertIn("spearman_rho", table.columns)


if __name__ == "__main__":
    unittest.main()
