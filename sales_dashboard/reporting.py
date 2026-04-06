from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .analysis import (
    aggregate_by_product,
    aggregate_by_region,
    calculate_kpis,
    daily_trend,
    rolling_trend,
)

CHART_TEMPLATE = "plotly_white"
PRIMARY_COLOR = "#0f766e"
SECONDARY_COLOR = "#d97706"
ACCENT_COLOR = "#1d4ed8"
HIGHLIGHT_COLOR = "#dc2626"


def build_volume_by_product_chart(dataframe: pd.DataFrame) -> go.Figure:
    grouped = aggregate_by_product(dataframe)
    fig = px.bar(
        grouped,
        x="label",
        y="qte",
        text_auto=".0f",
        title="Volume des ventes par produit",
        labels={"label": "Produit", "qte": "Quantité"},
        color_discrete_sequence=[PRIMARY_COLOR],
        template=CHART_TEMPLATE,
    )
    return _style_bar_chart(fig)


def build_revenue_by_product_chart(dataframe: pd.DataFrame) -> go.Figure:
    grouped = aggregate_by_product(dataframe)
    fig = px.bar(
        grouped,
        x="label",
        y="chiffre_affaires",
        text_auto=".0f",
        title="Chiffre d'affaires par produit",
        labels={"label": "Produit", "chiffre_affaires": "Chiffre d'affaires"},
        color_discrete_sequence=[SECONDARY_COLOR],
        template=CHART_TEMPLATE,
    )
    return _style_bar_chart(fig)


def build_revenue_by_region_chart(dataframe: pd.DataFrame) -> go.Figure:
    grouped = aggregate_by_region(dataframe)
    fig = px.bar(
        grouped,
        x="label",
        y="chiffre_affaires",
        text_auto=".0f",
        title="Chiffre d'affaires par région",
        labels={"label": "Région", "chiffre_affaires": "Chiffre d'affaires"},
        color_discrete_sequence=[ACCENT_COLOR],
        template=CHART_TEMPLATE,
    )
    return _style_bar_chart(fig)


def build_daily_trend_chart(dataframe: pd.DataFrame) -> go.Figure:
    grouped = daily_trend(dataframe)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=grouped["date"],
            y=grouped["qte"],
            name="Quantité",
            marker_color=PRIMARY_COLOR,
            opacity=0.7,
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=grouped["date"],
            y=grouped["chiffre_affaires"],
            name="Chiffre d'affaires",
            mode="lines+markers",
            line={"color": HIGHLIGHT_COLOR, "width": 3},
        ),
        secondary_y=True,
    )
    fig.update_layout(
        template=CHART_TEMPLATE,
        title="Tendance journalière",
        legend_title_text="Indicateurs",
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Quantité", secondary_y=False)
    fig.update_yaxes(title_text="Chiffre d'affaires", secondary_y=True)
    return fig


def build_rolling_trend_chart(dataframe: pd.DataFrame, window: int = 7) -> go.Figure:
    grouped = rolling_trend(dataframe, window=window)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=grouped["date"],
            y=grouped["chiffre_affaires"],
            name="CA journalier",
            mode="lines+markers",
            line={"color": PRIMARY_COLOR, "width": 1, "dash": "dot"},
            opacity=0.5,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=grouped["date"],
            y=grouped["ca_rolling"],
            name=f"Moy. mobile {window}j (CA)",
            mode="lines",
            line={"color": HIGHLIGHT_COLOR, "width": 3},
        )
    )
    fig.update_layout(
        template=CHART_TEMPLATE,
        title=f"Moyenne mobile {window} jours – Chiffre d'affaires",
        legend_title_text="Indicateurs",
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Chiffre d'affaires")
    return fig


def export_html_reports(dataframe: pd.DataFrame, output_dir: Union[str, Path]) -> None:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)

    figures = {
        "volume-par-produit.html": build_volume_by_product_chart(dataframe),
        "ca-par-produit.html": build_revenue_by_product_chart(dataframe),
        "ventes-par-region.html": build_revenue_by_region_chart(dataframe),
        "tendance-journaliere.html": build_daily_trend_chart(dataframe),
    }

    for filename, figure in figures.items():
        figure.write_html(target / filename, include_plotlyjs="cdn")


def write_summary_markdown(dataframe: pd.DataFrame, target_path: Union[str, Path]) -> None:
    target = Path(target_path)
    target.write_text(render_summary_markdown(dataframe), encoding="utf-8")


def render_summary_markdown(dataframe: pd.DataFrame) -> str:
    kpis = calculate_kpis(dataframe)
    product_table = aggregate_by_product(dataframe)
    region_table = aggregate_by_region(dataframe)

    lines = [
        "# Fiche synthèse – Dashboard ventes PME",
        "",
        "## Données",
        f"- Période: {kpis['date_debut']} -> {kpis['date_fin']}",
        f"- Lignes: {kpis['nb_transactions']}",
        "- Colonnes: date, produit, prix, qte, region",
        "- Règle métier: chiffre_affaires = prix * qte",
        "",
        "## KPI globaux",
        f"- Chiffre d'affaires total: {format_currency(kpis['chiffre_affaires_total'])}",
        f"- Quantité totale vendue: {format_number(kpis['qte_total'])}",
        f"- Nombre de produits: {kpis['nb_produits']}",
        f"- Nombre de régions: {kpis['nb_regions']}",
        "",
        "## Ventes par produit",
        "| Produit | Volume | CA | % volume | % CA |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for row in product_table.itertuples(index=False):
        lines.append(
            f"| {row.label} | {format_number(row.qte)} | "
            f"{format_currency(row.chiffre_affaires)} | "
            f"{format_percent(row.part_volume)} | {format_percent(row.part_chiffre_affaires)} |"
        )

    lines.extend(
        [
            "",
            "## Ventes par région",
            "| Région | Volume | CA | % volume | % CA |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for row in region_table.itertuples(index=False):
        lines.append(
            f"| {row.label} | {format_number(row.qte)} | "
            f"{format_currency(row.chiffre_affaires)} | "
            f"{format_percent(row.part_volume)} | {format_percent(row.part_chiffre_affaires)} |"
        )

    return "\n".join(lines) + "\n"


def dataframe_to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    export_frame = dataframe.copy()
    if "date" in export_frame.columns:
        export_frame["date"] = pd.to_datetime(export_frame["date"]).dt.strftime("%Y-%m-%d")
    return export_frame.to_csv(index=False).encode("utf-8")


def format_currency(value: float) -> str:
    return f"{format_number(value)} €"


def format_percent(value: float) -> str:
    return f"{float(value):.2f}%"


def format_number(value: float) -> str:
    numeric_value = float(value)
    if numeric_value.is_integer():
        return f"{int(numeric_value):,}".replace(",", " ")
    formatted = f"{numeric_value:,.2f}"
    return formatted.replace(",", " ").replace(".", ",")


def _style_bar_chart(fig: go.Figure) -> go.Figure:
    fig.update_layout(margin={"l": 10, "r": 10, "t": 60, "b": 10}, showlegend=False)
    return fig
