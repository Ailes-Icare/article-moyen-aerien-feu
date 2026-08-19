# Les données

Les fichiers à charger dans les outils. **Aucun outil ne les charge tout
seul** : vous cliquez sur un bouton d'import et vous désignez le fichier.

Quel fichier dans quel outil ? →
**[le tableau des imports](../5-documentation/02-tableau-des-imports.md)**

---

## `ecopage/`

| Fichier | Contenu |
|---|---|
| `flotte.json` | Le référentiel central : 14 aéronefs, dont 7 écopeurs dimensionnés. [Schéma détaillé](../5-documentation/10-referentiel-flotte.md) |
| `plans-eau-france.json` | 2 219 courses d'écopage sur 1 614 plans d'eau, 95 départements |
| `profils-vol-ecopage-v19.json` | 7 profils de vol dessinés, avec leurs réglages d'affichage |
| `fiches-appareil/` | 6 fiches d'un seul appareil, pour mise à jour ciblée |
| `axes-regionaux/` | Les 22 GeoJSON régionaux — **entrées** de la chaîne d'extraction, pas des fichiers à charger dans un outil |

## `pelicandromes/`

| Fichier | Contenu |
|---|---|
| `flotte-pelicandromes_5_1.json` | 12 appareils, champs orientés ravitaillement au sol |
| `chronologie-pelicandromes_4_1.json` | 33 sites : position, statut, historique daté |
| `parametres-utilisateur-pelicandromes.json` | Vos réglages d'affichage — position des étiquettes, couleurs |
| `carte2-data-v2.json` | Une couleur de risque par département et arrondissement |

## `statistiques/`

| Fichier | Source |
|---|---|
| `feu annee apres annee 2020-2025.json` | Bilan annuel français |
| `API_AG.LND.FRST.ZS_*.zip` | Banque mondiale — couvert forestier par pays |
| `API_AG.LND.TOTL.K2_*.zip` | Banque mondiale — surface des terres |
| `sdg_15_11$*.csv.gz` | Eurostat — indicateur SDG 15.11 |

Les trois archives sont des données brutes telles que téléchargées. Elles ne se
chargent dans aucun outil — ceux-ci embarquent déjà les données traitées — mais
documentent l'origine des chiffres.

---

## ⚠ Le piège des deux flottes

`flotte.json` et `flotte-pelicandromes_5_1.json` sont **deux référentiels
différents**, pas deux versions du même. Schémas incompatibles, 14 appareils
contre 12, champs sans rapport.

Les charger l'un à la place de l'autre ne provoque aucune erreur visible, mais
l'affichage se dégrade en silence. **Fiez-vous au dossier.**
