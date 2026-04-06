from __future__ import annotations

from pathlib import Path

try:
    import streamlit as st
except ModuleNotFoundError as exc:  # pragma: no cover - user-facing fallback
    raise SystemExit(
        "Streamlit n'est pas installé. Exécutez `python3 -m pip install -r requirements.txt`."
    ) from exc

from sales_dashboard.analysis import (
    DataValidationError,
    aggregate_by_product,
    aggregate_by_region,
    apply_filters,
    calculate_kpis,
    load_sales_data,
)
from sales_dashboard.reporting import (
    build_daily_trend_chart,
    build_revenue_by_product_chart,
    build_revenue_by_region_chart,
    build_rolling_trend_chart,
    build_volume_by_product_chart,
    dataframe_to_csv_bytes,
    format_currency,
    format_number,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "ventes.csv"


@st.cache_data(show_spinner=False)
def get_sales_data():
    return load_sales_data(DATA_PATH)


def main() -> None:
    st.set_page_config(page_title="Dashboard ventes PME", layout="wide")
    st.title("Dashboard ventes PME")
    st.caption(
        "Analyse interactive des ventes avec validation des données et indicateurs recalculés à la volée."
    )

    try:
        dataframe = get_sales_data()
    except DataValidationError as error:
        st.error(str(error))
        st.stop()

    filtered = render_filters(dataframe)
    if filtered.empty:
        st.warning("Aucune vente ne correspond aux filtres sélectionnés.")
        st.stop()

    kpis = calculate_kpis(filtered)
    render_overview(kpis)
    render_analysis_tables(filtered)

    tab_charts, tab_trends = st.tabs(["Visualisations", "Tendances"])
    with tab_charts:
        render_charts(filtered)
    with tab_trends:
        render_trends(filtered)

    render_detailed_table(filtered)


def render_filters(dataframe):
    st.sidebar.header("Filtres")
    min_date = dataframe["date"].min().date()
    max_date = dataframe["date"].max().date()

    date_range = st.sidebar.date_input(
        "Période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(date_range, tuple):
        start_date, end_date = date_range
    else:
        start_date = min_date
        end_date = date_range

    all_regions = sorted(dataframe["region"].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Régions",
        options=all_regions,
        default=all_regions,
    )

    all_products = sorted(dataframe["produit"].unique().tolist())
    selected_products = st.sidebar.multiselect(
        "Produits",
        options=all_products,
        default=all_products,
    )

    return apply_filters(
        dataframe,
        start_date=start_date,
        end_date=end_date,
        regions=selected_regions,
        products=selected_products,
    )


def render_overview(kpis) -> None:
    st.subheader("Vue d'ensemble")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Chiffre d'affaires", format_currency(kpis["chiffre_affaires_total"]))
    col2.metric("Quantité vendue", format_number(kpis["qte_total"]))
    col3.metric("Produits actifs", str(kpis["nb_produits"]))
    col4.metric("Régions actives", str(kpis["nb_regions"]))
    col5.metric("Produit leader", kpis["top_produit"] or "–")

    st.caption(
        f"Période filtrée: {kpis['date_debut']} -> {kpis['date_fin']} | "
        f"Transactions: {kpis['nb_transactions']}"
    )


def render_analysis_tables(dataframe) -> None:
    product_table = aggregate_by_product(dataframe).rename(columns={"label": "produit"})
    region_table = aggregate_by_region(dataframe).rename(columns={"label": "region"})

    with st.expander("Synthèse détaillée", expanded=True):
        left, right = st.columns(2)
        left.dataframe(product_table, use_container_width=True, hide_index=True)
        right.dataframe(region_table, use_container_width=True, hide_index=True)


def render_charts(dataframe) -> None:
    st.subheader("Visualisations")
    left, right = st.columns(2)
    left.plotly_chart(build_revenue_by_product_chart(dataframe), use_container_width=True)
    right.plotly_chart(build_volume_by_product_chart(dataframe), use_container_width=True)

    bottom_left, bottom_right = st.columns(2)
    bottom_left.plotly_chart(
        build_revenue_by_region_chart(dataframe), use_container_width=True
    )
    bottom_right.plotly_chart(build_daily_trend_chart(dataframe), use_container_width=True)


def render_trends(dataframe) -> None:
    window = st.slider("Fenêtre de moyenne mobile (jours)", min_value=3, max_value=14, value=7)
    st.plotly_chart(build_rolling_trend_chart(dataframe, window=window), use_container_width=True)


def render_detailed_table(dataframe) -> None:
    st.subheader("Détail des ventes")
    st.download_button(
        "Télécharger les données filtrées (CSV)",
        data=dataframe_to_csv_bytes(dataframe),
        file_name="ventes-filtrees.csv",
        mime="text/csv",
    )

    table = dataframe.copy()
    table["date"] = table["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(table, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
