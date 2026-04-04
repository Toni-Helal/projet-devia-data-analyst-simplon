<<<<<<< HEAD
# Dashboard ventes PME

Ce projet transforme une analyse CSV simple en dashboard Streamlit plus fiable, avec une couche de validation des données, des agrégations réutilisables et des artefacts de référence alignés entre Python et SQL.

## Fonctionnalités

- validation du fichier source `data/ventes.csv` avant tout calcul
- KPI recalculés selon les filtres sélectionnés
- graphiques Plotly pour produits, régions et tendance journalière
- export CSV des données filtrées dans l'interface
- requêtes SQL de référence cohérentes avec les calculs Python
- génération optionnelle des rapports HTML et de la fiche synthèse Markdown

## Données attendues

Le fichier CSV doit contenir exactement les colonnes suivantes :

- `date`
- `produit`
- `prix`
- `qte`
- `region`

Règle métier utilisée partout dans le projet :

`chiffre_affaires = prix * qte`

## Lancement local

Installer les dépendances :

```bash
python3 -m pip install -r requirements.txt
```

Lancer le dashboard :

```bash
streamlit run dashboard.py
```

## Génération des artefacts de référence

Cette commande régénère :

- `docs/fiche_synthese.md`
- les graphiques HTML dans `outputs/`
=======
# Analyse des ventes d’une PME – Projet Dev IA

## Contexte

Ce projet a pour objectif de réaliser une première analyse des ventes d’une PME à partir d’un extrait de données couvrant 20 jours d’activité.

L’analyse repose sur :
- SQL pour l’exploration et les calculs
- Python (Pandas + Plotly) pour la visualisation

---

## Données

Le jeu de données contient les colonnes suivantes :

- date  
- produit  
- prix  
- qte  
- region  

Hypothèse de calcul :  
Le chiffre d’affaires est défini comme :

CA = prix × qte

---

## Analyses SQL réalisées

Les requêtes SQL ont été exécutées sur sqliteonline et exportées.
Elles permettent de répondre aux questions suivantes :

1. Chiffre d’affaires total  
2. Ventes par produit (volume et chiffre d’affaires)  
3. Ventes par région (volume et chiffre d’affaires)  

Les requêtes sont disponibles dans :
`sql/queries.sql`

Les résultats synthétisés sont présentés dans :
`docs/fiche_synthese.md`

---

## Visualisations Python

Trois graphiques ont été développés à l’aide de Plotly :

- Ventes (volume) par région 
- Volume des ventes par produit  
- Chiffre d’affaires par produit  

Pour générer les visualisations :
>>>>>>> origin/main

```bash
python3 app.py
```

<<<<<<< HEAD
## Tests

```bash
python3 -m unittest discover -s tests
```

## Structure utile

```text
.
├── dashboard.py
├── app.py
├── sales_dashboard/
│   ├── analysis.py
│   └── reporting.py
├── data/
│   └── ventes.csv
├── docs/
│   └── fiche_synthese.md
├── outputs/
├── sql/
│   └── queries.sql
└── tests/
    └── test_analysis.py
```

## Notes

- le dashboard est l'interface principale du projet
- `app.py` reste un utilitaire de génération d'artefacts
- la source de vérité reste le CSV, sans base de données dans cette phase
- le dossier `.devcontainer` permet toujours une exécution guidée dans Codespaces
=======
---

## Structure du projet

Les fichiers HTML générés se trouvent dans :

`outputs/`

```
.
├── app.py
├── data/
│  └── ventes.csv
├── requirements.txt
├── sql/
│  └── queries.sql
├── docs/
│  └── fiche_synthese.md
├── outputs/
│  ├── ventes-par-region.html
│  ├── volume-par-produit.html
│  └── ca-par-produit.html
```

---

## Technologies utilisées
- Python 3  
- Pandas  
- Plotly  
- SQLite (sqliteonline)

Ce projet peut être exécuté localement (via Python 3 et `requirements.txt`) ou directement dans GitHub Codespaces grâce au dossier `.devcontainer`.

---

## Synthèse

Cette analyse permet :

- d’identifier les produits les plus performants,
- de comparer volume vendu et rentabilité,
- de repérer les régions générant le plus de chiffre d’affaires.

Le projet répond aux livrables demandés : export SQL, fiche synthèse et dépôt GitHub complété avec visualisations.

>>>>>>> origin/main

