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

```bash
python3 app.py
```

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

