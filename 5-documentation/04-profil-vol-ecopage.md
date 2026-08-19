# Profil de vol d'écopage

**Fichier** : [`1-outils/ecopage/profil-vol-ecopage-v18.html`](../1-outils/ecopage/profil-vol-ecopage-v18.html)
**À charger** : `2-donnees/ecopage/profils-vol-ecopage-v19.json`
**Accepte aussi** : `2-donnees/ecopage/flotte.json`

Cet outil dessine, à l'échelle et de profil, **ce que fait un avion quand il
écope** : l'approche, la descente, le contact avec l'eau, la remise de gaz, le
dégagement. Une seule vue, mais qui répond à la question que tout le monde se
pose — pourquoi faut-il une si grande étendue d'eau pour remplir un réservoir.

---

## Le modèle en trois phases

C'est le cœur de l'outil, et ce qui le distingue d'un schéma décoratif. Le
contact avec l'eau se décompose en trois temps :

| Phase | Ce qui se passe | Écopage |
|---|---|---|
| **Avant** | L'appareil touche l'eau et ralentit jusqu'à la vitesse d'écopage | **non efficace** |
| **Efficace** | Les écopes sont sorties, le réservoir se remplit | **efficace** |
| **Après** | Écopes rentrées, l'appareil accélère jusqu'à la rotation | **non efficace** |

La distinction compte parce que les documentations constructeur publient
souvent la **seule phase efficace** — 430 m pour tel appareil — alors que la
longueur d'eau réellement nécessaire est la somme des trois, plus les marges
d'approche et de dégagement.

Les distances se calculent en trapèze, la vitesse variant linéairement dans
chaque phase :

```
d_avant   = (v_touche + v_eco) / 2 × t_avant
d_efficace =  v_eco               × t_efficace
d_apres   = (v_eco + v_rotation) / 2 × t_apres
```

L'outil affiche **l'écart** entre la somme des phases et la course déclarée, au
lieu de l'absorber silencieusement. Un écart non nul signale une incohérence
dans les données, pas un défaut d'affichage.

---

## Le lien avec le référentiel

Le profil de vol ne vit pas seul : il lit `flotte.json`. Une table déclarative
de quinze lignes associe chaque champ du référentiel à l'endroit du profil qui
l'utilise, avec sa conversion d'unité.

Concrètement : si vous corrigez la vitesse d'approche du CL-415 dans l'éditeur
de flotte, le profil de vol la reprend au chargement suivant. L'outil signale
en évidence tout écart entre ce qu'il affiche et ce que dit le référentiel.

**Le référentiel fait autorité.** En cas de divergence, c'est `flotte.json` qui
a raison et le profil qui doit être corrigé.

---

## Les sections de l'interface

- **Profil actif / Profils enregistrés** — sept profils livrés, un par écopeur.
  Vous pouvez en créer, en dupliquer, en supprimer.
- **Appareil, couleurs, silhouette** — l'identité visuelle du profil.
- **Approche, décollage, seuils** — les angles et les vitesses de chaque phase.
- **Longueur d'écopage** — les trois phases, et la reconstitution qui en découle.
- **Distances** — l'origine de l'axe et les barres de seuil.
- **Mise en page** — légendes fléchées, trajectoire, échelle.
- **Poids / puissance** — le tableau comparatif des avions affichés.

---

## Le fichier v19

`profils-vol-ecopage-v19.json` est un fichier « tout-en-un » : il contient à la
fois les sept profils et les réglages d'affichage.

Sa nouveauté par rapport à la v18 est d'avoir extrait les réglages communs dans
une section `glob` — mise en page, couleurs, unités — sérialisés une seule fois
et appliqués à tous les appareils. Les copies par profil sont conservées pour
les anciens outils, mais **ignorées au chargement**.

---

## La version antérieure

`6-archives/versions-anterieures/profil-vol-ecopage-v17.html` est conservée
pour la traçabilité. Elle ne connaît pas le modèle en trois phases et confond
la phase efficace avec la course entière. **Ne vous en servez pas** pour
produire un chiffre.
