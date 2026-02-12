-- 3.a Chiffre d'affaires total
SELECT SUM(prix * qte) AS ca_total
FROM ventes;

-- 3.b Ventes par produit (volume + CA)
SELECT
  produit,
  SUM(qte) AS qte_totale,
  SUM(prix * qte) AS ca_total
FROM ventes
GROUP BY produit
ORDER BY ca_total DESC;

-- 3.c Ventes par région (volume + CA)
SELECT
  region,
  SUM(qte) AS qte_totale,
  SUM(prix * qte) AS ca_total
FROM ventes
GROUP BY region
ORDER BY ca_total DESC;
