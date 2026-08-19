# Tableau des imports — quel fichier dans quel outil

*La page à garder sous la main. Elle répond à la question la plus fréquente :
« qu'est-ce que je charge, et où ? »*

---

## Le tableau

| Outil | Bouton | Fichier à charger | Obligatoire ? |
|---|---|---|---|
| **plans-eau-ecopage** | 📂 Importer la flotte | `2-donnees/ecopage/flotte.json` | recommandé |
| | Importer des plans d'eau | `2-donnees/ecopage/plans-eau-france.json` | recommandé |
| **profil-vol-ecopage-v18** | Importer un JSON | `2-donnees/ecopage/profils-vol-ecopage-v19.json` | recommandé |
| | *(le même bouton)* | `2-donnees/ecopage/flotte.json` | facultatif |
| **editeur-flotte** | Importer un JSON de flotte | `2-donnees/ecopage/flotte.json` | **oui** |
| | Importer une fiche d'appareil | `2-donnees/ecopage/fiches-appareil/*.json` | facultatif |
| | Importer un CSV de MàJ | *(votre propre CSV)* | facultatif |
| **comparatif-poids-puissance** | Importer un JSON de flotte | `2-donnees/ecopage/flotte.json` | recommandé |
| **distance_pelicandrome_v11_1** | Importer flotte | `2-donnees/pelicandromes/flotte-pelicandromes_5_1.json` | recommandé |
| | Importer chronologie | `2-donnees/pelicandromes/chronologie-pelicandromes_4_1.json` | recommandé |
| | Importer du disque | `2-donnees/pelicandromes/parametres-utilisateur-pelicandromes.json` | facultatif |
| **cartographie-interactive-v18** | 📂 Importer la chronologie | `2-donnees/pelicandromes/chronologie-pelicandromes_4_1.json` | recommandé |
| | 📂 Importer JSON (Carte 2) | `2-donnees/pelicandromes/carte2-data-v2.json` | facultatif |
| **les 4 outils statistiques** | — | *aucun import* | — |

---

## Le piège à connaître

Il existe **deux référentiels de flotte différents**, et ils ne sont pas
interchangeables :

| | `flotte.json` | `flotte-pelicandromes_5_1.json` |
|---|---|---|
| Dossier | `2-donnees/ecopage/` | `2-donnees/pelicandromes/` |
| Appareils | 14 | 12 |
| Champs | écopage détaillé : `longueur_min_m`, `citerne_l`, phases de vol, sourçage | ravitaillement au sol : `speed`, `reload`, `range`, `qty` |
| Outils | écopage | pélicandromes |

Charger l'un dans les outils de l'autre ne provoque pas d'erreur visible, mais
les champs attendus manquent et l'affichage se dégrade sans prévenir. **Fiez-vous
au dossier** : `2-donnees/ecopage/` pour les outils d'écopage,
`2-donnees/pelicandromes/` pour les outils pélicandromes.

---

## Ordre de chargement

Quand un outil accepte plusieurs fichiers, l'ordre n'a pas d'importance, à une
exception près :

**Dans l'éditeur de flotte, chargez toujours le référentiel complet
(`flotte.json`) AVANT une fiche d'appareil.** Une fiche seule remplacerait la
flotte entière par un unique appareil. Chargée après, elle fusionne
proprement : l'éditeur détecte que le nom existe déjà et ouvre une fenêtre
d'arbitrage où vous choisissez, champ par champ, l'ancienne ou la nouvelle
valeur.

---

## Ce que fait chaque fichier, en détail

### `flotte.json` — le référentiel central

14 aéronefs, dont 7 écopeurs dimensionnés. Version 6.4 du schéma. Porte pour
chaque appareil ses dimensions, ses vitesses, ses prix, son profil de vol
d'écopage, et **la source de chaque valeur** — c'est la particularité du
fichier. → [schéma complet](10-referentiel-flotte.md)

### `plans-eau-france.json` — l'eau écopable

2 219 courses d'écopage réparties sur 1 614 plans d'eau, dans 95 départements.
Une « course » est un couloir rectiligne de 60 m de large où un appareil peut
descendre. Un grand plan d'eau en porte plusieurs : la Loire en compte 81,
l'estuaire 35, un étang une seule.
→ [comment il est produit](11-chaine-extraction.md)

### `profils-vol-ecopage-v19.json` — les profils dessinés

7 profils de vol, avec la géométrie de chaque phase et les réglages
d'affichage. Le fichier « tout-en-un » de l'outil de profil de vol : il
contient à la fois les données et la mise en page.

### `flotte-pelicandromes_5_1.json` — la flotte, vue sol

12 appareils avec les champs qui comptent pour le ravitaillement au sol :
vitesse de croisière, temps de rechargement, rayon d'action, quantité en parc.

### `chronologie-pelicandromes_4_1.json` — le réseau

33 sites avec leur position, leur statut courant (retardant fixe, mobile, eau
seule, en travaux, fermé, site de production) et leur historique daté. C'est le
fichier de référence unique du réseau.

### `parametres-utilisateur-pelicandromes.json` — vos réglages

Position des étiquettes sur la carte, couleurs par catégorie, taille de police,
réglages de l'outil de distance. Purement cosmétique : sans lui les outils
fonctionnent avec leurs valeurs par défaut.

### `carte2-data-v2.json` — le risque par territoire

Une couleur hexadécimale par code géographique. Le système est en poupée
russe : `"33"` colore toute la Gironde, `"33001"` ne colore que
l'arrondissement de Blaye. Les codes d'arrondissement sont les codes INSEE à
5 caractères, pas des codes à 3 chiffres.

### `fiches-appareil/*.json` — un appareil à la fois

Six fiches, une par appareil, au format attendu par l'éditeur de flotte. Elles
servent à faire travailler quelqu'un — ou une IA — sur un seul appareil, puis à
réintégrer le résultat sans risquer d'écraser le reste du référentiel.
