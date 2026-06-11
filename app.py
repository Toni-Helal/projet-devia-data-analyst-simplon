import plotly.express as px
import pandas as pd

# Charger les données
donnees = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-"
    "zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv"
)

# -----------------------------
# 1. Ventes par produit
# -----------------------------

ventes_par_produit = (
    donnees.groupby("produit", as_index=False)["qte"].sum()
)

figure_ventes = px.bar(
    ventes_par_produit,
    x="produit",
    y="qte",
    text="qte",
    title="Quantité vendue par produit",
    labels={
        "produit": "Produit",
        "qte": "Quantité vendue"
    }
)

figure_ventes.write_html("ventes-par-produit.html")

# -----------------------------
# 2. Chiffre d'affaires par produit
# -----------------------------

donnees["chiffre_affaires"] = donnees["prix"] * donnees["qte"]

ca_par_produit = (
    donnees.groupby("produit", as_index=False)["chiffre_affaires"].sum()
)

figure_ca = px.bar(
    ca_par_produit,
    x="produit",
    y="chiffre_affaires",
    text="chiffre_affaires",
    title="Chiffre d'affaires par produit",
    labels={
        "produit": "Produit",
        "chiffre_affaires": "Chiffre d'affaires (€)"
    }
)

figure_ca.write_html("chiffre-affaires-par-produit.html")

print("Les deux graphiques ont été générés avec succès !")