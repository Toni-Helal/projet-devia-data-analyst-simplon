<<<<<<< HEAD
from __future__ import annotations

from pathlib import Path

from sales_dashboard.analysis import DataValidationError, load_sales_data
from sales_dashboard.reporting import export_html_reports, write_summary_markdown

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "ventes.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
SUMMARY_PATH = BASE_DIR / "docs" / "fiche_synthese.md"


def main() -> int:
    try:
        dataframe = load_sales_data(DATA_PATH)
    except DataValidationError as error:
        print(error)
        return 1

    export_html_reports(dataframe, OUTPUT_DIR)
    write_summary_markdown(dataframe, SUMMARY_PATH)

    print("Artifacts updated:")
    print(f"- Summary: {SUMMARY_PATH}")
    print(f"- HTML reports: {OUTPUT_DIR}")
    print("Primary interface: streamlit run dashboard.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
=======
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/ventes.csv")

df["chiffre_affaires"] = df["prix"] * df["qte"]

# ---------
# Volume des ventes par produit
# ---------
volume_par_produit = (
    df.groupby("produit", as_index=False)["qte"].sum()
    .sort_values("qte", ascending=False)
)

fig_volume = px.bar(
    volume_par_produit,
    x="produit",
    y="qte",
    title="Volume des ventes par produit",
    text_auto=True
)
fig_volume.write_html("outputs/volume-par-produit.html")

# ---------
# Chiffre d'affaires par produit
# ---------
ca_par_produit = (
    df.groupby("produit", as_index=False)["chiffre_affaires"].sum()
    .sort_values("chiffre_affaires", ascending=False)
)

fig_ca = px.bar(
    ca_par_produit,
    x="produit",
    y="chiffre_affaires",
    title="Chiffre d’affaires par produit",
    text_auto=True
)
fig_ca.write_html("outputs/ca-par-produit.html")

# ---------
# Ventes (CA) par région  
# ---------
ca_par_region = (
    df.groupby("region", as_index=False)["chiffre_affaires"].sum()
    .sort_values("chiffre_affaires", ascending=False)
)

fig_region = px.bar(
    ca_par_region,
    x="region",
    y="chiffre_affaires",
    title="Chiffre d’affaires par région",
    text_auto=True
)
fig_region.write_html("outputs/ventes-par-region.html")

print("Graphiques générés avec succès (outputs/).")
>>>>>>> origin/main
