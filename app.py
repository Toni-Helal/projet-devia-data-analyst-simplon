import plotly.express as px
import pandas as pd

# Charger les données
données = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

# Additionner les quantités pour chaque produit
ventes_par_produit = (
    données.groupby("produit", as_index=False)["qte"].sum()
)

# Créer le graphique
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

figure = px.pie(données, values='qte', names='region', title='quantité vendue par région')


# Générer le fichier HTML
figure.write_html('ventes-par-region.html')

print('ventes-par-région.html généré avec succès !')
