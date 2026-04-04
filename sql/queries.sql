<<<<<<< HEAD
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
=======
-- 3.a Chiffre d'affaires total
SELECT SUM(prix * qte) AS ca_total
FROM ventes;

-- 3.b Ventes par produit (volume + CA)
>>>>>>> origin/main
SELECT
  produit,
  SUM(qte) AS volume_total,
  SUM(prix * qte) AS chiffre_affaires,
  ROUND(
<<<<<<< HEAD
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
=======
    (SUM(qte) * 100.0) / (SELECT SUM(qte) FROM ventes),
    2
  ) AS pourcentage_volume_total
FROM ventes
WHERE produit IN ('Produit A', 'Produit B', 'Produit C')
GROUP BY produit;


-- 3.c Ventes par région (volume + CA)
SELECT
  region,
  SUM(prix * qte) AS chiffre_affaires,
  SUM(qte) AS volume,
  ROUND(
    (SUM(qte) * 100.0) / NULLIF((SELECT SUM(qte) FROM ventes), 0),
  2) AS pourcentage_volume
>>>>>>> origin/main
FROM ventes
GROUP BY region
ORDER BY chiffre_affaires DESC;

<<<<<<< HEAD
=======

>>>>>>> origin/main
