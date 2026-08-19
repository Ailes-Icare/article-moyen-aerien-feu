# Les quatre outils statistiques

**Dossier** : [`1-outils/statistiques/`](../1-outils/statistiques/)
**À charger** : rien. Ces outils sont entièrement autonomes, données comprises.

Ils ne parlent pas des moyens aériens mais du **contexte** : combien brûle,
où, et comment la tendance évolue. Ils servent à situer les chiffres des autres
outils.

---

## Timeline Incendie France

`Timeline Incendie France.html` — *Visualisation DFCI : historique & impact,
2000-2025*

Une frise des vingt-cinq dernières années de feux en France : surfaces brûlées
année par année, événements marquants, ruptures.

C'est là qu'on voit ce que 2022 a représenté — un record absolu, plusieurs fois
la moyenne des années précédentes — et que le feu a débordé de ses terres
historiques : premiers incendies recensés dans des départements qui n'en
connaissaient pas.

---

## Département incendie sur 5 ans

Deux fichiers, deux versions :

- `departement incendie sur 5 ans.html` — la version d'origine
- `departement-incendie-5-ans-v2.html` — **la version à jour**

*Cartographie DFCI : impacts incendies vs couvert forestier*

Les surfaces brûlées par département, **rapportées au couvert forestier**.
C'est la nuance qui compte : un département très boisé qui brûle beaucoup n'est
pas dans la même situation qu'un département peu boisé qui brûle autant.

La v2 corrige des données et améliore le rendu. Les deux sont conservées parce
que la première a servi de base à des publications ; **servez-vous de la v2**.

---

## Feux en Europe : intensité et dynamique par pays

`europe-feux-par-pays.html` — *ce que chaque pays perd, et où la tendance
s'emballe*

Compare les pays européens sur deux axes : ce qu'ils perdent en valeur absolue,
et la pente de leur tendance. Un pays peut brûler beaucoup sans que la
situation se dégrade, et inversement — c'est le second axe qui porte
l'information intéressante.

---

## Feux européens : surfaces et émissions

`europe-feux-emissions.html` — *ce qu'ils brûlent, ce qu'ils rejettent*

Met en regard les surfaces brûlées et les **émissions de carbone** associées.
Le rapport entre les deux n'est pas constant : la nature du couvert et
l'intensité du feu changent beaucoup ce qu'une même surface rejette.

---

## Les sources

Le dossier [`2-donnees/statistiques/`](../2-donnees/statistiques/) conserve les
jeux de données publics utilisés :

| Fichier | Source | Contenu |
|---|---|---|
| `API_AG.LND.FRST.ZS_DS2_en_csv_v2_33175.zip` | Banque mondiale | Part du couvert forestier par pays |
| `API_AG.LND.TOTL.K2_DS2_en_csv_v2_249.zip` | Banque mondiale | Surface totale des terres par pays |
| `sdg_15_11$defaultview_linear_2_0.csv.gz` | Eurostat | Indicateur SDG 15.11, surface forestière |
| `feu annee apres annee 2020-2025.json` | compilation | Bilan annuel français, 2020 à 2025 |

Les trois premiers sont des archives brutes telles que téléchargées. Elles ne
se chargent pas dans les outils — ceux-ci embarquent déjà les données traitées
— mais elles documentent l'origine des chiffres et permettent de les
recalculer.

`feu annee apres annee 2020-2025.json` accompagne les deux outils français.
