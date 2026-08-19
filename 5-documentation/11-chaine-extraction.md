# La chaîne d'extraction des plans d'eau

**Dossier** : [`3-chaine-extraction/`](../3-chaine-extraction/)
**Produit** : `2-donnees/ecopage/plans-eau-france.json`

*Vous n'avez besoin de cette chaîne que pour **régénérer** les données
géographiques — par exemple avec un extrait OpenStreetMap plus récent. Pour
simplement utiliser les outils, le fichier est déjà là.*

---

## Ce qu'elle fait

Elle part des polygones d'eau d'OpenStreetMap et en tire des **courses
d'écopage** : des couloirs rectilignes de 60 m de large où un avion peut
descendre, se poser sur l'eau, se remplir et repartir.

Le résultat actuel : **2 219 courses sur 1 614 plans d'eau**, dans 95
départements.

---

## Les quatre étapes

```
   Geofabrik (OpenStreetMap)
            │
            │  telecharge_geofabrik.py        ~8 Go, 6 min
            ▼
   22 jeux de shapefiles régionaux
            │
            │  extrait_toutes.py              10 min, 4 régions de front
            │    └─ appelle traite_region.py sur chacune
            ▼
   22 GeoJSON d'axes régionaux
            │
            │  consolide_axes.py              quelques secondes
            ▼
   plans-eau-france.json
```

### 1. `telecharge_geofabrik.py` — récupérer la matière

```bash
python telecharge_geofabrik.py
```

Télécharge les 22 extraits régionaux, en extrait les seules couches utiles,
range, supprime l'archive. Environ 8 Go de transfert, 6 minutes sur une bonne
connexion, et 850 Mo restant sur le disque.

Trois choses à savoir :

- **Reprise.** Une région déjà extraite est sautée, et l'archive n'est effacée
  qu'après vérification que les cinq fichiers du shapefile sont présents.
  Relançable autant de fois que nécessaire.
- **Fichier `.part`.** L'archive ne prend son nom définitif qu'une fois le
  transfert complet, donc une coupure ne laisse jamais un zip tronqué qui
  passerait pour bon.
- **Deux couches conservées.** `gis_osm_water_a_free_1` est indispensable —
  c'est la couche des **surfaces**. `gis_osm_waterways_free_1` est celle des
  **lignes**, inutile au calcul actuel mais conservée pour de futurs travaux
  sur les embouchures.

> **Le piège du `_a_`.** Les deux noms de couche ne diffèrent que par ce
> caractère, `a` pour *area*. Prendre la couche des lignes au lieu de celle des
> surfaces ne provoque **aucune erreur** : le script calcule des aires, une
> ligne a une aire nulle, le filtre vide la table et le résultat est zéro axe.
> Un échec parfaitement silencieux.

Options : `python telecharge_geofabrik.py corse alsace` pour se limiter à
certaines régions, `--garder-zip` pour conserver les archives.

### 2. `traite_region.py` — mesurer une région

```bash
python traite_region.py chemin/gis_osm_water_a_free_1.shp "Pays de la Loire"
```

Le cœur géométrique. Pour chaque région :

1. **Filtrage** — exclusion des zones humides et des docks, projection en
   Lambert-93, suppression des mares de moins de 0,1 ha.
2. **Recollage** — les rivières arrivent en tronçons ; on recolle les polygones
   contigus en composantes connexes. Une union globale saturerait la mémoire
   au-delà de 40 000 polygones, d'où le passage par une adjacence spatiale.
3. **Érosion** — chaque composante est rétrécie de la moitié de la largeur
   requise, ce qui rend la marge latérale implicite.
4. **Balayage rotatif** — recherche des cordes inscrites, tous les 3°.

**Ce que fait le balayage, et pourquoi c'est important.** Il énumère tous les
segments admissibles, puis retient ceux dont les **milieux sont écartés d'au
moins `ECART_MIN_M`** — 5 000 m par défaut.

Ce critère décide de tout. Un lac rond rend une corde par angle, soixante en
tout, dont les milieux tombent tous sur le centre : c'est une seule ressource
vue soixante fois, et l'écartement la ramène à une. Un estuaire de 30 km rend
des milieux étalés sur 30 km : autant de ressources réelles, toutes conservées.

C'est la même logique que l'échantillonnage du trait de côte tous les 15 km :
une longue étendue couvre une distance, elle ne se résume pas à un point.

Réglages par variable d'environnement, sans toucher au code :
`AXES_ECART_M` pour l'écartement, `AXES_OUTDIR` pour le dossier de sortie.

### 3. `extrait_toutes.py` — lancer les 22

```bash
python extrait_toutes.py
```

Enchaîne `traite_region.py` sur toutes les régions téléchargées, quatre de
front. Une région déjà calculée est sautée ; un fichier illisible est refait.

Options : `-j 1` pour la série, `--refaire` pour tout recalculer, ou des noms
de région pour se limiter.

Compter environ 10 minutes au total. Rhône-Alpes et PACA sont les plus longues,
autour de 4 minutes chacune.

### 4. `consolide_axes.py` — assembler la France

```bash
python consolide_axes.py
```

Quatre opérations :

- **Dédoublonnage inter-régions.** Geofabrik livre les objets entiers, donc un
  plan d'eau à cheval sur deux régions est extrait des deux côtés. Le critère
  est physique : deux axes font double emploi si le milieu de l'un tombe à
  moins de 500 m de l'autre et qu'ils sont à peu près parallèles. Il ne
  s'applique **qu'entre fichiers régionaux différents** — un doublon
  intra-région est impossible par construction.
- **Affectation départementale**, avec une tolérance de 2 km qui rattrape
  l'imprécision du contour simplifié.
- **Retrait des glaciers.** L'extraction OSM prend les surfaces de glace pour
  des plans d'eau. Seuls les noms *commençant* par Glacier, Ghiacciaio,
  Glaciar, Gletscher, Nevero ou Vedretta sont retirés, pour ne pas emporter un
  lac qui contiendrait le mot par hasard.
- **Retrait du hors-territoire**, avec le Léman en exception nommée : son
  milieu tombe côté suisse, mais sa rive sud est française.

---

## Le banc de test

```bash
python test_courses.py
```

Huit contrôles sur des formes dont la réponse est connue. Quatre vérifient la
**non-régression** — un rectangle de 2 000 × 300 m avec une marge de 100 doit
rendre 1 903 m, un rectangle trop étroit doit être rejeté, un disque de rayon
800 doit rendre 1 499 m. Quatre vérifient le comportement multi-courses : le
disque doit rendre **une** course, le rectangle de 30 km doit en rendre
plusieurs, étalées sur au moins 80 % de sa longueur.

**Lancez-le après toute modification de la géométrie.** Il tourne en quelques
secondes.

---

## Prérequis

```bash
python -m pip install geopandas shapely pyproj
```

Environ 150 Mo de dépendances, la chaîne GDAL comprise. Python 3.9 ou plus
récent.

---

## Les axes régionaux livrés

[`2-donnees/ecopage/axes-regionaux/`](../2-donnees/ecopage/axes-regionaux/)
contient les 22 GeoJSON déjà produits. Ils permettent de relancer
`consolide_axes.py` — pour changer une règle de nettoyage, par exemple — **sans
retélécharger les 8 Go**.

Chaque axe y porte : son nom, sa longueur, la surface du plan d'eau,
l'identifiant du plan d'eau (`plan_eau`) et son rang (`rang`, 1 étant la plus
longue course).

> **Attention aux totaux de surface.** `aire_ha` décrit l'étendue entière et se
> répète donc sur chacune de ses courses. Pour totaliser une surface, ne sommez
> que les `rang == 1`, sans quoi un fleuve compte autant de fois qu'il a de
> courses.
