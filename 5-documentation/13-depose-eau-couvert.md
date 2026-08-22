# Dépose de l'eau dans le couvert

**Fichier** : [`1-outils/largage/depose-eau-couvert-v1.html`](../1-outils/largage/depose-eau-couvert-v1.html)
**À charger** : rien. L'outil est une illustration autonome, sans import.

Cet outil anime **trois largages d'un volume d'eau strictement identique** au-dessus
d'une futaie, et montre ce qui arrive réellement au sol. Seules changent la
vitesse sol et la durée d'ouverture des trappes — donc le **débit de sortie**.
La thèse, contre l'expression « effet de souffle » : à volume égal, c'est la
**concentration au sol** (le *coverage level*) qui décide qu'une ligne tienne,
et à CL appliqué identique, c'est le **débit** qui décide de la répartition
entre les cimes et le sol.

---

## Les trois cas

| Cas | Ce qui change | Ce qu'on observe |
|---|---|---|
| **1 — avion** | référence | le débit de référence, la ligne de référence |
| **2 — voilure tournante, deux fois plus lente** | même volume, même durée d'ouverture | même débit, mais concentré sur deux fois moins de distance : CL appliqué doublé, ligne deux fois plus courte |
| **3 — avion, trappes deux fois plus lentes** | même volume, durée d'ouverture doublée | même ligne que le cas 1, mais débit divisé par deux : la colonne se fragmente plus tôt, l'essentiel reste dans les cimes, le sol ne reçoit plus assez |

---

## Les quatre grandeurs

C'est la grille de lecture de tout largage, telle que l'outil l'affiche :

| Grandeur | Calcul | Ce qu'elle décide |
|---|---|---|
| Débit de sortie | Q = V / t | la pénétration dans le couvert |
| Longueur de ligne | L = v × t | la distance réellement traitée |
| **CL appliqué** | **Q / (v × largeur) / 0,41** | ce qu'on lâche sur la zone, avant interception |
| CL arrivé au sol | CL appliqué × taux de transmission | ce qui atteint les combustibles de surface |

Le *coverage level* est défini par le NWCG en gallons de retardant par
100 pieds carrés de surface au sol ; 1 CL = 0,41 L/m². La table de
prescription (CL 2 sur herbe, 3–4 sur maquis, 6–8 sur futaie) porte sur le
**combustible dominant** — on surcharge en haut pour qu'il en reste assez en
bas, car le couvert fermé intercepte une grande part de la charge.

## Le modèle embarqué

- Pénétration = (Q/Q_réf)^0,75 × (H_réf/h)^0,5, avec Q_réf = 2 400 L/s et
  H_réf = 40 m.
- La fragmentation est réduite à **deux classes de gouttes** (gros fragments
  qui traversent, fines gouttelettes qui dérivent), avec des probabilités de
  traversée par strate calibrées pour le contraste visuel, pas mesurées.
- Les réglages (volet « Réglages ») exposent les curseurs du modèle ; la
  vitesse de l'animation se règle (temps réel, demi, quart) et « Valeurs par
  défaut » réinitialise tout.

---

## Ce que l'outil simplifie

À lire avant de citer quoi que ce soit — l'outil le dit lui-même dans ses
notes de bas de page :

- **C'est une illustration, pas un outil de dimensionnement.** Aucun chiffre
  affiché ne doit être repris comme une mesure.
- Le **seuil de CL 2 retenu au sol** est une transposition de l'auteur, pas un
  standard publié : la prescription officielle porte sur le CL appliqué,
  jamais sur ce qui subsiste sous couvert.
- Les échelles verticale et horizontale ne sont pas homogènes ; l'appareil
  n'est à l'échelle de rien.
- La hauteur de largage — paramètre dominant dans la réalité — est tenue
  constante pour isoler l'effet du débit ; son influence est modélisée
  grossièrement.
- Ni vent, ni colonne convective, ni pente ; largeur de nappe uniforme.

## Le contexte

L'outil rappelle les deux réserves émises par la DGSCGC sur l'A400M
(manœuvrabilité en relief accidenté, efficacité du concept d'« extinction par
effet de souffle ») et remet le largage à sa place : l'apport des moyens
aériens dans l'extinction dépasse rarement **5 à 7 %**. Un largage ralentit un
front, protège un point sensible, ouvre une fenêtre aux équipes au sol — il
n'éteint pas.

Les sources (NWCG, USDA Forest Service, *Fire Safety Journal*, etc.) sont
listées avec liens en bas de la page de l'outil.
