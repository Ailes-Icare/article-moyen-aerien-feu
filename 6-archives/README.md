# Archives — versions antérieures

**Ne vous servez pas de ces fichiers.** Ils sont conservés pour la traçabilité :
ils ont servi à produire des publications, et il faut pouvoir retrouver ce
qu'ils disaient. Mais ils portent tous des données ou des méthodes corrigées
depuis.

Pour chacun, ce qui a changé et où trouver le remplaçant.

---

## Outils

### `profil-vol-ecopage-v17.html`
**Remplacé par** `1-outils/ecopage/profil-vol-ecopage-v18.html`

La v17 ne connaît pas le modèle d'écopage en trois phases : elle confond la
phase efficace avec la course entière. Les longueurs d'eau qu'elle affiche sont
donc sous-estimées.

### `plans-eau-ecopage.AVANT-multi.html`
**Remplacé par** `1-outils/ecopage/plans-eau-ecopage.html`

Version d'avant deux changements majeurs. D'une part elle ne connaît qu'**un
axe par plan d'eau** : la Loire y pèse autant qu'un étang. D'autre part son
score territorial additionne des courses et du littoral, ce qui produisait des
départements colorés en vert sans aucun point d'eau visible.

### `cartographie-interactive-v13.html` et `v16_1.html`
**Remplacées par** `1-outils/pelicandromes/cartographie-interactive-v18.html`

Antérieures à des corrections du réseau : des sites y sont classés « utilisation
limitée » alors qu'ils sont fermés de fait depuis le retrait des Tracker, le
site de production du retardant n'y figure pas, et plusieurs implantations
créées en 2020 sont absentes.

### `distance_pelicandrome_v3.html` et `v9.html`
**Remplacées par** `1-outils/pelicandromes/distance_pelicandrome_v11_1.html`

Mêmes corrections de réseau, plus l'artifice de fusion des cercles qui n'existe
que depuis la v10.

---

## Données

### `flotte (1).json`
**Fusionné dans** `2-donnees/ecopage/flotte.json`

C'était la version la plus à jour à un moment donné, d'où son nom de doublon de
téléchargement. Son contenu a été fusionné dans le référentiel canonique, avec
au passage la correction d'une valeur aberrante et la migration de 47
commentaires vers le schéma de sourçage.

### `plans-eau-france.AVANT-multi.json`
**Remplacé par** `2-donnees/ecopage/plans-eau-france.json`

1 540 axes, un seul par plan d'eau. Le fichier actuel en compte 2 219, répartis
sur 1 614 plans d'eau.

### `chronologie-pelicandromes_3.json`
**Remplacé par** `2-donnees/pelicandromes/chronologie-pelicandromes_4_1.json`

Version 3, moins de sites et statuts non corrigés.

### `flotte-pelicandromes.json`
**Remplacé par** `2-donnees/pelicandromes/flotte-pelicandromes_5_1.json`

10 appareils au lieu de 12. Contient en plus une section `pelicandromes` qui a
depuis été extraite dans le fichier de chronologie, seul référentiel du réseau.

---

## Scripts

### `traite_region_ORIGINAL.py`
**Remplacé par** `3-chaine-extraction/traite_region.py`

La version d'origine, telle que récupérée. Elle ne retient qu'**une seule
course par plan d'eau** — la plus longue corde inscrite — et écrit sa sortie
sans préciser l'encodage, ce qui produit du cp1252 sous Windows.

Conservée parce qu'elle sert de référence de non-régression : le rang 1 de la
version actuelle doit lui être identique, géométrie comprise. C'est vérifié sur
les 22 régions.

### `gemini-code-1787015560089.py`
**Piste abandonnée**

Un concept d'extraction alternatif, fondé sur la BD TOPAGE du Sandre plutôt que
sur OpenStreetMap. Jamais mené à terme. Conservé parce qu'il documente une voie
explorée : la BD TOPAGE fait autorité et serait plus propre qu'OSM, mais elle
se télécharge par département et pèse bien plus lourd.
