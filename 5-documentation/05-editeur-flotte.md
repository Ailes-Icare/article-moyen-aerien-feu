# Éditeur de flotte

**Fichier** : [`1-outils/ecopage/editeur-flotte.html`](../1-outils/ecopage/editeur-flotte.html)
**À charger** : `2-donnees/ecopage/flotte.json` — **obligatoire**

C'est **l'outil qui fait autorité** pour modifier `flotte.json`. Les autres
outils lisent le référentiel ; celui-ci l'écrit. Toute correction de donnée
devrait passer par lui, parce qu'il connaît le schéma, les valeurs autorisées
et les champs dérivés.

---

## Le principe : chaque valeur porte sa source

C'est la convention centrale du référentiel. Un champ numérique est accompagné
de deux compagnons :

```json
"vitesse_ecopage_kmh": 130,
"vitesse_ecopage_kmh_src": "constructeur",
"vitesse_ecopage_kmh_commentaire": "manuel de vol, édition 2019"
```

Le suffixe `_src` prend ses valeurs dans un **vocabulaire fermé** :

| Valeur | Signification | Considérée comme |
|---|---|---|
| `constructeur` | documentation du constructeur | **trouvée** |
| `publie` | source publique identifiée | **trouvée** |
| `estime` | estimation raisonnée | interprétée |
| `interpole` | déduite d'appareils voisins | interprétée |
| `analogie` | reprise d'un appareil comparable | interprétée |
| `concept` | valeur de projet, appareil non volant | interprétée |
| `calcul` | dérivée d'autres champs par l'outil | interprétée |

Les valeurs interprétées sont marquées d'un astérisque dans les outils. C'est
ce qui permet de distinguer, d'un coup d'œil, ce qui est documenté de ce qui
est déduit.

---

## Ce qui se saisit et ce qui se calcule

Certains champs sont **dérivés** et affichés en lecture seule. Les modifier n'a
pas de sens : ils se recalculent.

Pour chaque phase d'écopage, on saisit **soit la durée, soit la distance** ;
l'autre se déduit. Les totaux et `longueur_min_m` sont toujours dérivés.

`longueur_min_m` suit une règle formelle : **la moyenne entre le cycle le plus
court et le cycle le plus long, tous deux mesurés au seuil pratique de 50 m**.
Elle est intégralement automatique — vous ne la saisissez jamais.

---

## Les trois imports

### Un référentiel complet

`2-donnees/ecopage/flotte.json`. Remplace tout. C'est le point de départ normal.

### Une fiche d'appareil

`2-donnees/ecopage/fiches-appareil/CL215_improved.json` par exemple.

**Chargez toujours le référentiel complet d'abord.** Une fiche seule
remplacerait la flotte entière par un appareil unique.

Si le nom de l'appareil existe déjà, l'éditeur **ne l'écrase pas
silencieusement**. Il ouvre une fenêtre d'arbitrage qui liste, champ par champ,
l'ancienne valeur et la nouvelle, avec leur source respective. Vous choisissez.

Cette fenêtre existe pour une raison précise : elle évite qu'un travail
d'amélioration mené à côté — par vous ou par quelqu'un d'autre — soit perdu
sans qu'on s'en aperçoive au moment de réimporter.

### Un CSV de mise à jour

Pour corriger un même champ sur plusieurs appareils d'un coup. L'éditeur
affiche un écran de validation avant d'appliquer quoi que ce soit.

---

## Le champ moteur

Deux champs distincts, à ne pas confondre :

- `moteur_nombre` — combien de moteurs
- `moteur_ref` — la référence exacte, par exemple `Pratt & Whitney PW123AF`

La puissance est un troisième champ. Une référence moteur ne se déduit pas
d'une puissance, et inversement : c'est pourquoi ils sont séparés.

---

## Après l'édition

Exportez. Le fichier produit remplace `2-donnees/ecopage/flotte.json`.

Les autres outils ne se mettent pas à jour tout seuls : rechargez le nouveau
fichier dans chacun. Le profil de vol vous signalera tout écart persistant.
