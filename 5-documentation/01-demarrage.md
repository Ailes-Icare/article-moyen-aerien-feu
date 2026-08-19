# Démarrage — ouvrir son premier outil

*Cette fiche part de zéro. Si vous savez déjà ouvrir un fichier HTML, sautez
directement au [tableau des imports](02-tableau-des-imports.md).*

---

## 1. Ce qu'est un outil de ce dépôt

Un fichier `.html` unique. Pas d'installation, pas de serveur, pas de connexion
Internet. Tout est à l'intérieur : le code, les bibliothèques graphiques, les
polices de caractères, les fonds de carte, et un jeu de données par défaut.

C'est pour cela qu'un fichier pèse parfois plus d'un mégaoctet. C'est normal.

## 2. L'ouvrir

Double-cliquez dessus. Il s'ouvre dans votre navigateur.

Si le double-clic ouvre un éditeur de texte au lieu du navigateur, faites un
clic droit → *Ouvrir avec* → votre navigateur.

**Navigateurs conseillés** : Chrome, Edge ou Firefox, à jour. Les outils
utilisent des fonctions récentes ; un navigateur de plus de trois ans peut
échouer silencieusement.

## 3. Charger des données

Chaque outil affiche des données par défaut, embarquées à l'intérieur. Elles
peuvent être **plus anciennes** que celles du dossier `2-donnees/`.

Pour charger les données à jour, cherchez un bouton commençant par 📂, du genre
« Importer la flotte » ou « Importer des plans d'eau ». Cliquez, désignez le
fichier, c'est fait.

Quel fichier pour quel bouton ? Tout est dans le
[tableau des imports](02-tableau-des-imports.md). C'est la page à garder sous
la main.

## 4. Trois choses qui surprennent au début

**Rien n'est enregistré.** Fermez l'onglet et vos réglages sont perdus. Les
outils qui gèrent des réglages ont un bouton d'export : servez-vous-en avant de
fermer.

**Un mauvais fichier ne casse rien**, mais ne fait rien. Si vous chargez la
chronologie des pélicandromes dans l'outil des plans d'eau, il vous le dira ou
ignorera le fichier. Aucun risque de corrompre quoi que ce soit — les fichiers
du dossier `2-donnees/` ne sont jamais modifiés par un outil.

**Les images d'appareils viennent d'Internet.** C'est la seule exception à
l'autonomie complète : les photos des fiches sont référencées par leur adresse
web. Sans connexion, les fiches s'affichent sans photo, le reste fonctionne.

## 5. Exporter une image

Plusieurs outils ont des boutons 📷 qui produisent un PNG de la zone affichée.
Les images sont calibrées pour une largeur de page de 1 200 pixels et restent
lisibles une fois réduites à 800, la largeur d'affichage de LinkedIn.

Dans l'outil des plans d'eau, un bouton peut aussi produire une **vidéo** MP4
d'un balayage animé. Voir sa [fiche](03-plans-eau-ecopage.md).

## 6. Un parcours pour découvrir

1. Ouvrez **[plans-eau-ecopage.html](../1-outils/ecopage/plans-eau-ecopage.html)**.
   Chargez `2-donnees/ecopage/flotte.json`, puis
   `2-donnees/ecopage/plans-eau-france.json`.
2. Cochez le Canadair CL-415 dans la liste des appareils. La carte se colore :
   vert là où l'eau est proche, rouge là où elle est loin.
3. Basculez en haut sur **Par territoire**. La carte cesse de parler d'un avion
   et dit, pour chaque département, à quelle distance moyenne se trouve l'eau
   utilisable.
4. Faites glisser le curseur de longueur minimale. Regardez les couleurs se
   dégrader à mesure que les petits plans d'eau sortent du jeu.

En un quart d'heure vous aurez compris l'essentiel de la logique du projet :
un appareil exige une certaine longueur d'eau, et cette exigence détermine à
elle seule la géographie de ce qu'il peut faire.

---

## Où aller ensuite

- [Le tableau des imports](02-tableau-des-imports.md) — quel fichier dans quel outil
- [La fiche de chaque outil](../README.md#les-outils-en-une-phrase-chacun)
- [Les conventions et les limites](12-conventions-et-limites.md) — à lire avant de citer un chiffre
