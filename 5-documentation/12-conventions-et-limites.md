# Conventions et limites connues

*À lire avant de citer un chiffre de ce dépôt.*

---

## Ce que sont ces outils

Des **instruments d'étude informels**. Ils ne constituent ni une documentation
opérationnelle, ni un avis technique autorisé. Ils servent à comprendre des
ordres de grandeur et à fabriquer des illustrations argumentées.

Les chiffres qu'ils produisent sont, presque partout, des **bornes hautes de
candidats** : ce qui serait possible si rien d'autre ne s'y opposait.

---

## Les limites du recensement des plans d'eau

Ne sont **pas** pris en compte :

- la **profondeur** — un plan d'eau assez long peut être trop peu profond ;
- les **obstacles** — ponts, câbles, lignes électriques, pylônes ;
- le **dégagement d'approche** — relief, obstacles en bout de course ;
- le **marnage estival** — un plan d'eau de printemps peut être une vasière en
  août, précisément quand on en aurait besoin ;
- la **réglementation** — zones protégées, interdictions locales, usages
  concurrents.

Subsistent volontairement dans le jeu de données des **bassins portuaires** et
des **étangs côtiers** : géométriquement corrects, douteux à l'usage. Les
retirer aurait supposé un jugement au cas par cas qui n'a pas été fait.

### La limite du dédoublonnage

Le script de consolidation retire environ 215 doublons inter-régions. Le
fichier historique en annonçait 184 sur un corpus plus petit, mais sa règle est
perdue.

À l'essai, toute règle assez lâche pour en retirer autant **fusionne aussi des
étangs voisins bien distincts** — les étangs camarguais du Fangassier, du
Galabert et de la Dame, par exemple, qui sont serrés mais séparés. Le compte
retenu est donc plus prudent, et l'écart est assumé plutôt que masqué.

### La limite qui reste ouverte

Le seuil d'écartement de 5 000 m entre deux courses d'un même plan d'eau est un
choix, pas une mesure. Le réduire multiplie les courses sur les grandes
étendues ; l'augmenter les raréfie.

À 1 000 m, le Léman pesait 32 % de la longueur d'axe nationale — un seul lac,
majoritairement suisse. À 5 000 m il en pèse 12,5 %, pour 14 % de la surface
d'eau française. Le réglage retenu est celui qui donne la lecture la plus
équilibrée, mais il reste discutable.

---

## Les conventions techniques des outils

### Aucune dépendance réseau

C'est une règle absolue du projet : **aucun CDN, jamais**. Les bibliothèques
graphiques, les polices et les fonds de carte sont embarqués dans chaque
fichier HTML. C'est ce qui explique leur poids, et ce qui garantit qu'ils
fonctionneront encore dans dix ans, hors ligne.

Seule exception : les **photos d'appareils** sont référencées par leur adresse
web. Sans connexion, les fiches s'affichent sans photo.

### Aucun chargement automatique

Aucun outil ne va chercher un fichier tout seul. Tout import est explicite,
par un sélecteur de fichier. Vous savez donc toujours quelle donnée est
affichée — et les fichiers du dossier `2-donnees/` ne sont jamais modifiés par
un outil.

### Les captures sont calibrées pour 800 px

Les images produites par les boutons 📷 le sont depuis une page de 1 200 px de
large, pour un affichage LinkedIn à 800 px. Les polices des zones capturées
sont doublées par rapport au reste de l'interface, sans quoi elles tomberaient
sous 8 px une fois l'image réduite.

### Le sourçage

Toute valeur numérique du référentiel de flotte porte sa provenance, dans un
vocabulaire fermé de sept valeurs. `constructeur` et `publie` valent
« trouvée » ; les cinq autres valent « interprétée » et sont marquées d'un
astérisque dans les outils. Voir la
[fiche du référentiel](10-referentiel-flotte.md#la-convention-de-sourçage).

---

## Les données de risque de la cartographie

`carte2-data-v2.json` mérite une mise en garde particulière.

La donnée d'origine est une **grille climatique**, pas une table administrative.
Il n'existe aucune donnée officielle « par arrondissement » derrière cette
carte. Les valeurs ont été obtenues en géoréférençant la figure publiée puis en
échantillonnant la classe dominante de chaque arrondissement — une
interprétation reproductible, assumée comme telle.

Deux zones de moindre confiance : la moitié nord, où le moutonnement fin des
classes rend la majorité parfois limite, et les arrondissements minuscules ou
côtiers, où l'échantillon de pixels est maigre.

---

## Les pièges déjà rencontrés

Ils sont consignés ici parce qu'ils se reproduisent facilement.

| Piège | Comment il se manifeste |
|---|---|
| **La couche `_a_`** | Prendre `gis_osm_waterways` (lignes) au lieu de `gis_osm_water_a` (surfaces) donne zéro axe, sans aucune erreur |
| **L'encodage de sortie** | Un script Python qui écrit sans `encoding="utf-8"` produit du cp1252 sous Windows et de l'UTF-8 sous Linux |
| **Les codes d'arrondissement** | Ce sont les codes INSEE à 5 caractères, pas des codes à 3 chiffres ; une dérogation mal codée est ignorée en silence |
| **Les deux référentiels de flotte** | `flotte.json` et `flotte-pelicandromes*.json` ne sont pas interchangeables |
| **La surface répétée** | `aire_ha` se répète sur chaque course d'un même plan d'eau ; ne sommer que les `rang == 1` |
| **La fiche avant le référentiel** | Charger une fiche d'appareil avant `flotte.json` remplace la flotte entière par un seul appareil |
| **Chercher un nom, pas un comportement** | Avant de créer un mécanisme, chercher s'il existe déjà — sous un autre nom |

---

## Pour aller plus loin

`PROJET-reference.md`, dans ce même dossier, est le manuel technique historique
du projet. Il s'adresse à qui veut **modifier** les outils : conventions de
code, blocs de données embarquées, décisions datées et journal de travail.
