-- Vérifier les données importées
SELECT *
FROM ventes;

-- Compter le nombre de lignes
SELECT COUNT(*) AS nombre_lignes
FROM ventes;

-- Calculer le chiffre d'affaires total
SELECT SUM(prix * qte) AS chiffre_affaires_total
FROM ventes;

-- Calculer les ventes et le chiffre d'affaires par produit
SELECT
    produit,
    SUM(qte) AS quantite_vendue,
    SUM(prix * qte) AS chiffre_affaires
FROM ventes
GROUP BY produit
ORDER BY chiffre_affaires DESC;

-- Calculer les ventes par région
SELECT
    region,
    SUM(qte) AS quantite_vendue
FROM ventes
GROUP BY region
ORDER BY quantite_vendue DESC;