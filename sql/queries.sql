-- 1. Chiffre d'affaires total
SELECT SUM(prix * qte) AS chiffre_affaires_total
FROM ventes;

-- 2. Ventes par produit (volume + CA + parts)
WITH totaux AS (
  SELECT
    SUM(qte) AS volume_total,
    SUM(prix * qte) AS chiffre_affaires_total
  FROM ventes
)
SELECT
  produit,
  SUM(qte) AS volume_total,
  SUM(prix * qte) AS chiffre_affaires,
  ROUND(
    SUM(qte) * 100.0 / NULLIF((SELECT volume_total FROM totaux), 0),
    2
  ) AS part_volume,
  ROUND(
    SUM(prix * qte) * 100.0 / NULLIF((SELECT chiffre_affaires_total FROM totaux), 0),
    2
  ) AS part_chiffre_affaires
FROM ventes
GROUP BY produit
ORDER BY chiffre_affaires DESC;

-- 3. Ventes par région (volume + CA + parts)
WITH totaux AS (
  SELECT
    SUM(qte) AS volume_total,
    SUM(prix * qte) AS chiffre_affaires_total
  FROM ventes
)
SELECT
  region,
  SUM(qte) AS volume_total,
  SUM(prix * qte) AS chiffre_affaires,
  ROUND(
    SUM(qte) * 100.0 / NULLIF((SELECT volume_total FROM totaux), 0),
    2
  ) AS part_volume,
  ROUND(
    SUM(prix * qte) * 100.0 / NULLIF((SELECT chiffre_affaires_total FROM totaux), 0),
    2
  ) AS part_chiffre_affaires
FROM ventes
GROUP BY region
ORDER BY chiffre_affaires DESC;

