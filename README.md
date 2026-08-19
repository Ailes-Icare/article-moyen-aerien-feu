# Moyens aériens de lutte contre les feux de forêt — outils d'étude

Ce dépôt rassemble une dizaine d'outils cartographiques et d'analyse consacrés
aux **moyens aériens français de lutte contre les feux de forêt** : la flotte
d'avions bombardiers d'eau, les plans d'eau où ils écopent, et le réseau des
pélicandromes où ils se ravitaillent en retardant.

Tous les outils sont des **pages HTML autonomes**. Vous n'avez rien à
installer, rien à compiler, aucun serveur à lancer : vous ouvrez le fichier
dans votre navigateur et il fonctionne. Aucun ne fait appel à Internet.

---

## Par où commencer

**Vous découvrez le dépôt ?** Lisez
[5-documentation/01-demarrage.md](5-documentation/01-demarrage.md). Cinq
minutes suffisent pour ouvrir votre premier outil.

**Vous cherchez quel fichier charger dans quel outil ?** C'est la question la
plus fréquente, et elle a sa propre page :
[5-documentation/02-tableau-des-imports.md](5-documentation/02-tableau-des-imports.md).

**Vous voulez comprendre un outil précis ?** Chaque outil a sa fiche, listée
plus bas.

---

## Ce que contient le dépôt

```
1-outils/            les pages HTML à ouvrir            11 outils
2-donnees/           les fichiers à y charger           39 fichiers
3-chaine-extraction/ les scripts Python qui produisent   5 scripts
                     les données géographiques
4-articles/          les textes rédigés                  2 articles
5-documentation/     ce que vous lisez                  14 fiches
6-archives/          les versions antérieures           12 fichiers
```

Le détail dossier par dossier est en bas de cette page.

---

## Les outils, en une phrase chacun

### Écopage — la flotte amphibie et l'eau

| Outil | Ce qu'il montre |
|---|---|
| **[plans-eau-ecopage.html](1-outils/ecopage/plans-eau-ecopage.html)** | Où se trouve l'eau écopable en France, et à quelle distance elle est de n'importe quel point du territoire. → [fiche](5-documentation/03-plans-eau-ecopage.md) |
| **[profil-vol-ecopage-v18.html](1-outils/ecopage/profil-vol-ecopage-v18.html)** | Le profil de vol d'un écopage, phase par phase, à l'échelle. → [fiche](5-documentation/04-profil-vol-ecopage.md) |
| **[editeur-flotte.html](1-outils/ecopage/editeur-flotte.html)** | L'outil qui fait autorité pour modifier le référentiel des appareils. → [fiche](5-documentation/05-editeur-flotte.md) |
| **[comparatif-ecopeurs-poids-puissance.html](1-outils/ecopage/comparatif-ecopeurs-poids-puissance.html)** | Le rapport poids/puissance des écopeurs, et son effet sur le cycle. → [fiche](5-documentation/06-comparatif-poids-puissance.md) |

### Pélicandromes — le ravitaillement en retardant

| Outil | Ce qu'il montre |
|---|---|
| **[distance_pelicandrome_v11_1.html](1-outils/pelicandromes/distance_pelicandrome_v11_1.html)** | La couverture du territoire par le réseau des pélicandromes. → [fiche](5-documentation/07-distance-pelicandrome.md) |
| **[cartographie-interactive-v18.html](1-outils/pelicandromes/cartographie-interactive-v18.html)** | Le risque d'incendie projeté, superposé au réseau. → [fiche](5-documentation/08-cartographie-interactive.md) |

### Statistiques — le contexte

| Outil | Ce qu'il montre |
|---|---|
| **[Timeline Incendie France.html](1-outils/statistiques/Timeline%20Incendie%20France.html)** | L'historique des feux français de 2000 à 2025. |
| **[departement-incendie-5-ans-v2.html](1-outils/statistiques/departement-incendie-5-ans-v2.html)** | Les surfaces brûlées par département, rapportées au couvert forestier. |
| **[europe-feux-par-pays.html](1-outils/statistiques/europe-feux-par-pays.html)** | Ce que chaque pays européen perd au feu, et où la tendance s'emballe. |
| **[europe-feux-emissions.html](1-outils/statistiques/europe-feux-emissions.html)** | Surfaces brûlées et émissions de carbone associées. |

Ces quatre-là sont détaillés dans
[5-documentation/09-outils-statistiques.md](5-documentation/09-outils-statistiques.md).

---

## Les données, en une phrase chacune

| Fichier | Ce qu'il contient |
|---|---|
| **[flotte.json](2-donnees/ecopage/flotte.json)** | Le référentiel des 14 aéronefs : dimensions, vitesses, prix, sources. C'est le fichier central. → [schéma détaillé](5-documentation/10-referentiel-flotte.md) |
| **[plans-eau-france.json](2-donnees/ecopage/plans-eau-france.json)** | 2 219 courses d'écopage mesurées sur 1 614 plans d'eau. → [comment il est produit](5-documentation/11-chaine-extraction.md) |
| **[profils-vol-ecopage-v19.json](2-donnees/ecopage/profils-vol-ecopage-v19.json)** | Les 7 profils de vol dessinés, avec leurs réglages d'affichage. |
| **[flotte-pelicandromes_5_1.json](2-donnees/pelicandromes/flotte-pelicandromes_5_1.json)** | Le référentiel de flotte propre aux outils pélicandromes (schéma différent). |
| **[chronologie-pelicandromes_4_1.json](2-donnees/pelicandromes/chronologie-pelicandromes_4_1.json)** | Les 33 pélicandromes : position, statut, date de création ou de fermeture. |
| **[parametres-utilisateur-pelicandromes.json](2-donnees/pelicandromes/parametres-utilisateur-pelicandromes.json)** | Vos réglages d'affichage : position des étiquettes, couleurs, taille de police. |
| **[carte2-data-v2.json](2-donnees/pelicandromes/carte2-data-v2.json)** | La couleur de risque de chaque département et arrondissement. |

---

## Ce qu'il faut savoir avant de s'en servir

**Aucun outil ne charge de fichier tout seul.** Vous devez cliquer sur un
bouton d'import et désigner le fichier. C'est volontaire : vous savez ainsi
toujours quelle donnée est affichée. Le corollaire est qu'un outil ouvert sans
rien charger affiche ses données par défaut, embarquées à l'intérieur, qui
peuvent être plus anciennes que celles du dossier `2-donnees/`.

**Un mauvais fichier dans un outil ne casse rien**, mais ne fait rien non plus.
Le [tableau des imports](5-documentation/02-tableau-des-imports.md) dit
exactement quel fichier va où.

**Rien n'est enregistré automatiquement.** Si vous modifiez des réglages ou des
données dans un outil, exportez-les avant de fermer l'onglet.

**Les chiffres sont des bornes hautes, pas des vérités opérationnelles.** Les
plans d'eau recensés ignorent la profondeur, les ponts, les câbles et le
marnage estival. Les limites connues sont listées dans
[5-documentation/12-conventions-et-limites.md](5-documentation/12-conventions-et-limites.md),
et il faut les avoir lues avant de citer un chiffre.

---

## L'arborescence en détail

### `1-outils/` — les pages à ouvrir

Onze fichiers HTML autonomes, rangés par sujet : `ecopage/`,
`pelicandromes/`, `statistiques/`. Chacun pèse entre 300 Ko et 1,3 Mo, parce
qu'il embarque tout ce dont il a besoin — bibliothèques graphiques, polices,
fonds de carte, données par défaut.

### `2-donnees/` — les fichiers à charger

Rangés selon les mêmes trois sujets.

`ecopage/axes-regionaux/` contient les 22 fichiers GeoJSON produits région par
région par la chaîne d'extraction. Ce sont les **entrées** de
`consolide_axes.py`, pas des fichiers à charger dans un outil.

`ecopage/fiches-appareil/` contient six fiches d'un seul appareil, au format
attendu par l'éditeur de flotte. Elles servent à mettre à jour un appareil sans
toucher au reste du référentiel.

`statistiques/` contient trois archives de données publiques — Banque mondiale
pour le couvert forestier et la surface des pays, Eurostat pour l'indicateur
SDG 15.11. Elles documentent l'origine des chiffres des outils statistiques.

### `3-chaine-extraction/` — les scripts Python

Cinq scripts qui produisent `plans-eau-france.json` à partir des données
OpenStreetMap. Vous n'en avez besoin que si vous voulez **régénérer** les
données géographiques. Pour simplement utiliser les outils, ignorez ce dossier.
Le mode d'emploi complet est dans
[5-documentation/11-chaine-extraction.md](5-documentation/11-chaine-extraction.md).

### `4-articles/` — les textes

Deux articles rédigés à partir de ces outils, conservés parce qu'ils exposent
les raisonnements et les sources.

### `5-documentation/` — les fiches

Une fiche par outil, plus les fiches transversales. `PROJET-reference.md` est
le manuel historique du projet : plus technique, il s'adresse à quelqu'un qui
veut **modifier** les outils, pas seulement s'en servir.

### `6-archives/versions-anterieures/` — l'historique

Douze fichiers superseded, conservés pour la traçabilité. **Ne vous en servez
pas** : ils portent des données ou des méthodes corrigées depuis. Le détail de
ce qui a changé est dans
[6-archives/README.md](6-archives/README.md).

---

## Ce qui n'est pas dans le dépôt, et pourquoi

**Les shapefiles Geofabrik** (850 Mo). Ce sont les données OpenStreetMap
brutes dont la chaîne d'extraction se nourrit. Elles se retéléchargent en une
commande, voir la fiche de la chaîne d'extraction.

**`export.geojson`** (2,2 Mo). Un export Overpass d'un premier essai dont la
requête filtrait `water=lake|reservoir|lagoon|basin` — ce qui excluait
`water=river`, donc tous les cours d'eau larges. C'est pourquoi l'estuaire de
la Loire en était absent. Impasse identifiée et corrigée ; le fichier n'a plus
d'usage.

---

*Les outils de ce dépôt sont des instruments d'étude informels. Ils ne
constituent ni une documentation opérationnelle, ni un avis technique
autorisé.*
