# Distance Pélicandrome — couverture de la flotte

**Fichier** : [`1-outils/pelicandromes/distance_pelicandrome_v11_1.html`](../1-outils/pelicandromes/distance_pelicandrome_v11_1.html)
**À charger** : `flotte-pelicandromes_5_1.json` et `chronologie-pelicandromes_4_1.json`
**Facultatif** : `parametres-utilisateur-pelicandromes.json`

Cet outil traite du **ravitaillement au sol**, pas de l'écopage. Un
pélicandrome est une station qui remplit un avion de **retardant** — un produit
qui ralentit la propagation du feu — ou parfois d'eau seule. L'appareil s'y
pose, contrairement à l'écopage.

---

## Ce qu'il montre

La carte colore le territoire par **temps de rotation complète** : le
va-et-vient feu → pélicandrome → feu, avec le temps de rechargement au sol.
Vert là où c'est rapide, rouge là où l'éloignement pénalise la cadence.

Le cadre *Décomposition d'une rotation* détaille où passe le temps : vol aller,
manœuvres au sol, rechargement, vol retour. C'est souvent le rechargement qui
surprend — quelques minutes qui pèsent lourd sur une rotation courte.

---

## Le réseau et son histoire

`chronologie-pelicandromes_4_1.json` est le **fichier de référence unique du
réseau** : 33 sites avec, pour chacun, sa position, son statut courant et son
historique daté.

Les statuts distinguent :

| Statut | Ce que c'est |
|---|---|
| retardant fixe | station permanente avec cuves de retardant |
| mobile | camion-citerne déployable en quelques heures sur un parking d'aérodrome |
| eau seule | remplissage à l'eau, sans retardant |
| en travaux | site en cours d'aménagement |
| fermé | site désaffecté, conservé pour l'histoire |
| production | l'unité qui fabrique le retardant |

Ce dernier statut ne concerne qu'un seul point en France, ce qui est en soi un
fait notable : le retardant national dépend d'un site industriel unique.

Un curseur d'année rejoue l'évolution du réseau. Les sites apparaissent et
disparaissent à leur date, et un panneau commente les événements de chaque
année.

---

## Les paramètres utilisateur

`parametres-utilisateur-pelicandromes.json` conserve ce que vous avez réglé :
la position de chaque étiquette sur la carte, les couleurs par catégorie, la
taille de police, les réglages de distance.

Purement cosmétique — l'outil fonctionne sans — mais indispensable si vous
voulez retrouver une mise en page soignée d'une session à l'autre. Le bouton
**Importer du disque** le recharge ; un bouton d'export le sauvegarde.

C'est ce fichier qui explique que les étiquettes ne se chevauchent pas sur les
captures publiées : leur position a été réglée à la main, une fois, puis
conservée.

---

## L'artifice d'affichage

L'outil fusionne les cercles de portée qui se recouvrent en une seule forme,
avec un contour propre et une transparence maîtrisée, au lieu d'empiler des
disques dont les opacités s'additionnent. C'est ce qui rend la carte lisible
quand une quinzaine de stations se recouvrent.

Cette mécanique a servi de modèle à l'outil des plans d'eau, qui la reprend.

---

## Attention au référentiel de flotte

`flotte-pelicandromes_5_1.json` n'est **pas** `flotte.json`. Schéma différent,
12 appareils au lieu de 14, champs orientés ravitaillement au sol — vitesse,
temps de rechargement, rayon d'action, quantité en parc.

Charger `flotte.json` ici ne produit pas d'erreur visible, mais l'affichage se
dégrade sans prévenir. Voir le
[tableau des imports](02-tableau-des-imports.md#le-piège-à-connaître).

---

## Les versions antérieures

`distance_pelicandrome_v3.html` et `v9.html` sont dans les archives. La v11.1
est la seule à jour ; les deux autres portent des données de réseau corrigées
depuis.
