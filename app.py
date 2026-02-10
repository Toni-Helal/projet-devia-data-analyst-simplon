import pandas as pd
import plotly.express as px

# Charger les données
url = "URL_DU_FICHIER_CSV"
df = pd.read_csv("ventes.csv")

# ---------
# Volume des ventes par produit
# ---------
volume_par_produit = (
    df
    .groupby("produit")["qte"]
    .sum()
    .reset_index()
)

fig_volume = px.bar(
    volume_par_produit,
    x="produit",
    y="qte",
    title="Volume des ventes par produit"
)

fig_volume.write_html("volume-par-produit.html")

# ---------
# Chiffre d'affaires par produit
# ---------
df["chiffre_affaires"] = df["prix"] * df["qte"]

ca_par_produit = (
    df
    .groupby("produit")["chiffre_affaires"]
    .sum()
    .reset_index()
)

fig_ca = px.bar(
    ca_par_produit,
    x="produit",
    y="chiffre_affaires",
    title="Chiffre d’affaires par produit"
)

fig_ca.write_html("ca-par-produit.html")

print("Graphiques générés avec succès.")
