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
