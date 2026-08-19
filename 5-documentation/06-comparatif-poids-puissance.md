# Comparatif écopeurs — poids / puissance & cycle d'écopage

**Fichier** : [`1-outils/ecopage/comparatif-ecopeurs-poids-puissance.html`](../1-outils/ecopage/comparatif-ecopeurs-poids-puissance.html)
**À charger** : `2-donnees/ecopage/flotte.json`

Le plus simple des outils d'écopage : un tableau et quelques graphiques qui
mettent en regard la **masse**, la **puissance installée** et les
**conséquences sur le cycle d'écopage**.

---

## La question qu'il pose

Un écopeur doit faire trois choses difficiles à concilier : se poser sur l'eau
à faible vitesse, se remplir de plusieurs tonnes en quelques secondes, puis
redécoller alourdi d'autant. Le rapport poids/puissance décide de la troisième,
et c'est souvent lui qui fixe la longueur d'eau nécessaire — pas la capacité du
réservoir.

L'outil rend ce lien visible : deux appareils de citerne comparable peuvent
exiger des plans d'eau très différents selon ce qu'ils ont sous le capot.

---

## Ce qu'il affiche

- La **masse à vide** et la **masse maximale au décollage** de chaque écopeur.
- La **puissance installée**, avec le nombre de moteurs et leur référence.
- Le **rapport** des deux, à vide et en charge.
- La **capacité de citerne**, et le gain de masse qu'elle représente.
- Le **cycle d'écopage** qui en découle, à distance feu ↔ eau fixée.

Les valeurs interprétées portent un astérisque, selon la convention de sourçage
décrite dans la [fiche de l'éditeur](05-editeur-flotte.md).

---

## Sa place dans le projet

C'est un outil de **vérification croisée**. Il ne produit pas de donnée : il lit
`flotte.json` et met en évidence les incohérences que le tableau seul ne
révélerait pas — une puissance qui ne cadre pas avec une masse, un cycle qui ne
cadre pas avec une longueur d'eau exigée.

Quand un chiffre du référentiel change, c'est ici qu'on voit vite s'il tient
debout par rapport aux autres.
