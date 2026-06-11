import plotly.express as px
import pandas as pd

donnees = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-"
    "zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv"
)

ventes_par_produit = (
    donnees.groupby("produit", as_index=False)["qte"].sum()
)

figure = px.bar(
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

figure.write_html("ventes-par-produit.html")

print("ventes-par-produit.html généré avec succès !")