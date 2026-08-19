# Plans d'eau écopables & couverture de la flotte amphibie

**Fichier** : [`1-outils/ecopage/plans-eau-ecopage.html`](../1-outils/ecopage/plans-eau-ecopage.html)
**À charger** : `2-donnees/ecopage/flotte.json` puis `2-donnees/ecopage/plans-eau-france.json`

C'est l'outil le plus développé du dépôt. Il répond à deux questions
différentes, et la bascule tout en haut de la page dit laquelle.

---

## Les deux lectures de la carte

### Par appareil — ce que peut faire un avion donné

Vous cochez un ou plusieurs écopeurs. La carte affiche les plans d'eau **qu'ils
peuvent utiliser** — pas tous les plans d'eau existants — et colore le
territoire par temps de cycle : vert là où l'aller-retour feu ↔ eau est court,
rouge là où il s'allonge.

Le cycle se décompose en quatre réglages, dans le cadre *Paramètres de
rotation* : manœuvre d'écopage, manœuvre de largage, distance feu ↔ eau, et
cycle maximum affiché. Les deux derniers sont **couplés** : bouger l'un déplace
l'autre, puisqu'à cadence fixée une distance impose un cycle et réciproquement.

### Par territoire — ce que vaut un département, sans appareil

Aucun avion n'intervient. La couleur répond à une seule question : **si un feu
part ici, à quelle distance est l'eau utilisable ?**

Le territoire est échantillonné tous les 8 km — 8 526 points — et chaque point
cherche la course la plus proche, frontières départementales ignorées, parce
qu'un avion ne les voit pas.

Cette mesure a trois propriétés qui comptent :

- **Elle est absolue.** Une distance en kilomètres, pas un rang. L'échelle de
  couleur ne bouge ni avec le seuil, ni avec le département isolé, ni avec les
  autres départements. Deux captures prises à des réglages différents se
  comparent directement.
- **Elle est monotone.** Monter le seuil de longueur ne peut que *retirer* des
  sources d'eau, donc la distance ne peut qu'augmenter. Un département ne peut
  que se dégrader. Vérifié sur 3 168 comparaisons : zéro recul.
- **Elle voit la répartition.** Vingt étangs groupés dans un coin ne valent pas
  vingt étangs répartis. Un simple comptage ne faisait pas la différence.

Deux sous-lectures : **Distance moyenne** (le cas courant) et **Pire coin du
département** (le 90ᵉ centile — le coin mal desservi, pas le maximum absolu
qu'un point aberrant suffirait à dicter).

---

## Le curseur de longueur minimale

C'est le réglage qui commande tout : il décide **quelle eau compte**.

Une course de 700 m existe, mais aucun écopeur français ne peut s'en servir.
Les sept appareils dimensionnés exigent entre 1 524 et 2 185 m. Sous le
curseur, une rangée de boutons **« Caler sur : »** pose directement l'exigence
de chaque appareil. L'arrondi se fait au pas *supérieur* : le CL-415 demande
1 773 m et le curseur se pose à 1 800, jamais 1 750, pour ne pas laisser passer
des courses trop courtes pour lui.

---

## Le curseur d'exigence, tout en haut

Séparé des autres, dans le bandeau de bascule. Il permet de **détendre à la
main** l'exigence en longueur d'un appareil : 100 % rend la valeur du
référentiel, 0 % ramène tout le monde à 700 m.

À quoi ça sert : `longueur_min_m` est une *déduction*, pas une donnée
constructeur. Ce curseur permet de voir ce que gagnerait un appareil moins
exigeant, sans rien écrire dans le JSON — et le texte sous le curseur le
rappelle.

| Curseur | Exigence CL-415 | Courses accessibles |
|---|---|---|
| 100 % | 1 773 m | 510 |
| 50 % | 1 237 m | 916 |
| 0 % | 700 m | 2 219 |

Il est délibérément placé **hors des zones de capture** : c'est un réglage
d'étude, il n'a rien à faire sur une image publiée. Sa conséquence, elle,
s'affiche partout — titre, indicateurs, fiche d'identité — sinon une image
capturée contredirait la carte.

---

## Le trait de côte

La mer est une source d'eau comme une autre, échantillonnée tous les 15 km le
long du littoral. La case **Écopage en mer** la fait entrer ou sortir du
calcul, y compris du score territorial.

C'est un point à connaître : décochez-la et l'Ille-et-Vilaine passe de 5 à 0 à
un seuil de 4 000 m, parce que son score venait entièrement du rivage. La
façade maritime rapproche l'eau des zones côtières, et d'elles seules.

---

## Le regroupement

Par défaut, les plans d'eau proches se regroupent en un point portant leur
nombre. Décoché — la case est dans le cadre *Lecture par territoire* — chaque
course se dessine à sa vraie géométrie, un trait d'une extrémité à l'autre. Un
fleuve apparaît alors comme une chaîne de traits, ce qu'il est réellement.

Le regroupement reste imposé en lecture par appareil, où les traits se
superposeraient aux cercles de rotation.

---

## Les captures

| Bouton | Contenu |
|---|---|
| 📷 Carte + paramètres de rotation | Les deux premiers cadres en une seule image |
| 📷 Carte d'identité | La fiche de l'appareil sélectionné |
| 📷 Toutes les fiches | Toute la flotte affichée |
| 📷 Tableau comparatif | Le tableau global |

Chaque image porte une marge de 10 px et un nom de fichier préfixé par le
sujet. Les polices des zones capturées sont **doublées** par rapport au reste
de l'interface : les images finissent affichées en 800 px sur LinkedIn alors
que la page en fait 1 200, donc réduites d'un tiers.

### La vidéo

Cochez **filmer** à côté des lectures. Le bouton de capture de la carte devient
un enregistreur : il rejoue le balayage du seuil et produit une **vidéo** au
lieu d'une image. Seule la carte est filmée, c'est le seul élément qui bouge.

Format MP4 si le navigateur sait l'écrire, WebM sinon. Chaque palier doit être
rastérisé, ce qui coûte environ une seconde et demie **en plus** du délai
choisi : un balayage de 700 à 4 000 m par pas de 100 m dure près d'une minute.

---

## Ce que l'outil ne dit pas

Les courses recensées sont des **candidats géométriques**. Ne sont pris en
compte ni la profondeur, ni les ponts, ni les câbles et lignes électriques, ni
le dégagement d'approche, ni le marnage estival. Un bassin portuaire ou un
étang côtier peut y figurer alors qu'il est inutilisable en pratique.

Voir [12-conventions-et-limites.md](12-conventions-et-limites.md) pour la liste
complète.
