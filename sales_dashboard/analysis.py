from __future__ import annotations

from pathlib import Path
from typing import Mapping, Optional, Sequence, Union

import pandas as pd

REQUIRED_COLUMNS = ("date", "produit", "prix", "qte", "region")
TEXT_COLUMNS = ("produit", "region")
NUMERIC_COLUMNS = ("prix", "qte")


class DataValidationError(ValueError):
    """Raised when the source dataset cannot be analysed safely."""


def load_sales_data(csv_path: Union[str, Path]) -> pd.DataFrame:
    """Load the CSV dataset and validate its schema and values."""
    dataframe = pd.read_csv(csv_path)
    _validate_required_columns(dataframe.columns)

    cleaned = dataframe.copy()
    issues = []

    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    invalid_dates = int(cleaned["date"].isna().sum())
    if invalid_dates:
        issues.append(f"date: {invalid_dates} valeur(s) invalides ou vides")

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
        invalid_values = int(cleaned[column].isna().sum())
        if invalid_values:
            issues.append(
                f"{column}: {invalid_values} valeur(s) non numériques ou vides"
            )

    for column in TEXT_COLUMNS:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        invalid_values = int((cleaned[column].isna() | (cleaned[column] == "")).sum())
        if invalid_values:
            issues.append(f"{column}: {invalid_values} valeur(s) vides")

    if not issues:
        negative_prices = int((cleaned["prix"] < 0).sum())
        if negative_prices:
            issues.append(f"prix: {negative_prices} valeur(s) négatives")

        negative_quantities = int((cleaned["qte"] < 0).sum())
        if negative_quantities:
            issues.append(f"qte: {negative_quantities} valeur(s) négatives")

    if issues:
        raise DataValidationError("Jeu de données invalide:\n- " + "\n- ".join(issues))

    cleaned["chiffre_affaires"] = cleaned["prix"] * cleaned["qte"]
    cleaned = cleaned.sort_values(["date", "produit", "region"]).reset_index(drop=True)
    return cleaned


def apply_filters(
    dataframe: pd.DataFrame,
    start_date: Optional[object] = None,
    end_date: Optional[object] = None,
    regions: Optional[Sequence[str]] = None,
    products: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """Return a filtered copy of the dataset."""
    filtered = dataframe.copy()

    if start_date is not None:
        filtered = filtered.loc[filtered["date"] >= pd.Timestamp(start_date)]

    if end_date is not None:
        filtered = filtered.loc[filtered["date"] <= pd.Timestamp(end_date)]

    if regions is not None:
        if len(regions) == 0:
            return filtered.iloc[0:0].copy()
        filtered = filtered.loc[filtered["region"].isin(regions)]

    if products is not None:
        if len(products) == 0:
            return filtered.iloc[0:0].copy()
        filtered = filtered.loc[filtered["produit"].isin(products)]

    return filtered.reset_index(drop=True)


def calculate_kpis(dataframe: pd.DataFrame) -> Mapping[str, object]:
    """Compute the headline indicators displayed in the dashboard."""
    if dataframe.empty:
        return {
            "chiffre_affaires_total": 0.0,
            "qte_total": 0.0,
            "nb_produits": 0,
            "nb_regions": 0,
            "nb_transactions": 0,
            "date_debut": None,
            "date_fin": None,
        }

    return {
        "chiffre_affaires_total": float(dataframe["chiffre_affaires"].sum()),
        "qte_total": float(dataframe["qte"].sum()),
        "nb_produits": int(dataframe["produit"].nunique()),
        "nb_regions": int(dataframe["region"].nunique()),
        "nb_transactions": int(len(dataframe)),
        "date_debut": dataframe["date"].min().date(),
        "date_fin": dataframe["date"].max().date(),
    }


def aggregate_by_product(dataframe: pd.DataFrame) -> pd.DataFrame:
    grouped = _aggregate_dimension(dataframe, "produit")
    if grouped.empty:
        return grouped
    return grouped.rename(columns={"produit": "label"})


def aggregate_by_region(dataframe: pd.DataFrame) -> pd.DataFrame:
    grouped = _aggregate_dimension(dataframe, "region")
    if grouped.empty:
        return grouped
    return grouped.rename(columns={"region": "label"})


def daily_trend(dataframe: pd.DataFrame) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(columns=["date", "qte", "chiffre_affaires"])

    grouped = (
        dataframe.groupby("date", as_index=False)[["qte", "chiffre_affaires"]]
        .sum()
        .sort_values("date")
    )
    return grouped.reset_index(drop=True)


def _aggregate_dimension(dataframe: pd.DataFrame, dimension: str) -> pd.DataFrame:
    if dataframe.empty:
        return pd.DataFrame(
            columns=[
                dimension,
                "qte",
                "chiffre_affaires",
                "part_volume",
                "part_chiffre_affaires",
            ]
        )

    grouped = (
        dataframe.groupby(dimension, as_index=False)[["qte", "chiffre_affaires"]]
        .sum()
        .sort_values("chiffre_affaires", ascending=False)
        .reset_index(drop=True)
    )

    total_quantity = grouped["qte"].sum()
    total_revenue = grouped["chiffre_affaires"].sum()

    grouped["part_volume"] = grouped["qte"].div(total_quantity).mul(100).round(2)
    grouped["part_chiffre_affaires"] = (
        grouped["chiffre_affaires"].div(total_revenue).mul(100).round(2)
    )
    return grouped


def _validate_required_columns(columns: Sequence[str]) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing_columns:
        joined = ", ".join(missing_columns)
        raise DataValidationError(f"Colonnes manquantes: {joined}")
