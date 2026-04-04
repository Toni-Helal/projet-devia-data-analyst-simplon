from __future__ import annotations

import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path

from sales_dashboard.analysis import (
    DataValidationError,
    aggregate_by_product,
    aggregate_by_region,
    apply_filters,
    calculate_kpis,
    daily_trend,
    load_sales_data,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "ventes.csv"
SQL_PATH = BASE_DIR / "sql" / "queries.sql"


class SalesAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataframe = load_sales_data(DATA_PATH)

    def test_valid_dataset_produces_expected_global_metrics(self):
        kpis = calculate_kpis(self.dataframe)

        self.assertEqual(kpis["chiffre_affaires_total"], 44825.0)
        self.assertEqual(kpis["qte_total"], 3380.0)
        self.assertEqual(kpis["nb_produits"], 3)
        self.assertEqual(kpis["nb_regions"], 2)
        self.assertEqual(kpis["nb_transactions"], 39)

    def test_missing_required_column_raises_explicit_error(self):
        with self.assertRaisesRegex(DataValidationError, "Colonnes manquantes: region"):
            self._load_temporary_csv(
                [
                    ["date", "produit", "prix", "qte"],
                    ["2022-01-01", "Produit A", "10", "5"],
                ]
            )

    def test_non_numeric_values_raise_explicit_error(self):
        with self.assertRaisesRegex(DataValidationError, "qte: 1 valeur\\(s\\) non numériques"):
            self._load_temporary_csv(
                [
                    ["date", "produit", "prix", "qte", "region"],
                    ["2022-01-01", "Produit A", "10", "abc", "Nord"],
                ]
            )

    def test_negative_values_raise_explicit_error(self):
        with self.assertRaisesRegex(DataValidationError, "prix: 1 valeur\\(s\\) négatives"):
            self._load_temporary_csv(
                [
                    ["date", "produit", "prix", "qte", "region"],
                    ["2022-01-01", "Produit A", "-10", "5", "Nord"],
                ]
            )

    def test_filters_keep_kpis_and_aggregations_consistent(self):
        filtered = apply_filters(
            self.dataframe,
            start_date="2022-01-10",
            end_date="2022-01-15",
            regions=["Nord"],
            products=["Produit A", "Produit C"],
        )

        kpis = calculate_kpis(filtered)
        product_table = aggregate_by_product(filtered)
        trend_table = daily_trend(filtered)

        self.assertEqual(kpis["chiffre_affaires_total"], 4100.0)
        self.assertEqual(kpis["qte_total"], 340.0)
        self.assertEqual(len(filtered), 4)
        self.assertEqual(product_table["qte"].sum(), kpis["qte_total"])
        self.assertEqual(product_table["chiffre_affaires"].sum(), kpis["chiffre_affaires_total"])
        self.assertEqual(trend_table["qte"].sum(), kpis["qte_total"])
        self.assertEqual(trend_table["chiffre_affaires"].sum(), kpis["chiffre_affaires_total"])

    def test_sql_reference_matches_python_aggregations(self):
        connection = sqlite3.connect(":memory:")
        connection.execute(
            """
            CREATE TABLE ventes (
                date TEXT,
                produit TEXT,
                prix REAL,
                qte REAL,
                region TEXT
            )
            """
        )

        with DATA_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = [
                (
                    row["date"],
                    row["produit"],
                    float(row["prix"]),
                    float(row["qte"]),
                    row["region"],
                )
                for row in reader
            ]

        connection.executemany("INSERT INTO ventes VALUES (?, ?, ?, ?, ?)", rows)

        statements = [statement.strip() for statement in SQL_PATH.read_text().split(";") if statement.strip()]

        sql_total = connection.execute(statements[0]).fetchone()[0]
        product_rows = connection.execute(statements[1]).fetchall()
        region_rows = connection.execute(statements[2]).fetchall()

        python_kpis = calculate_kpis(self.dataframe)
        python_products = aggregate_by_product(self.dataframe)
        python_regions = aggregate_by_region(self.dataframe)

        self.assertEqual(sql_total, python_kpis["chiffre_affaires_total"])
        self.assertEqual(len(product_rows), len(python_products))
        self.assertEqual(len(region_rows), len(python_regions))
        self.assertEqual(product_rows[0][0], python_products.iloc[0]["label"])
        self.assertEqual(product_rows[0][1], python_products.iloc[0]["qte"])
        self.assertEqual(product_rows[0][2], python_products.iloc[0]["chiffre_affaires"])
        self.assertEqual(region_rows[0][0], python_regions.iloc[0]["label"])
        self.assertEqual(region_rows[0][1], python_regions.iloc[0]["qte"])
        self.assertEqual(region_rows[0][2], python_regions.iloc[0]["chiffre_affaires"])

    def _load_temporary_csv(self, rows):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", suffix=".csv") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows)
            handle.flush()
            load_sales_data(handle.name)


if __name__ == "__main__":
    unittest.main()
