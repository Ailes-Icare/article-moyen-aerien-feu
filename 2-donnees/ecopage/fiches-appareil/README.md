# Fiches d'un seul appareil

Six fichiers au schéma de `flotte.json`, mais ne portant qu'**un seul
appareil**. Ils servent à confier l'amélioration d'un appareil à quelqu'un — ou
à une IA — sans lui donner le référentiel entier, puis à réintégrer le résultat.

| Fichier | Appareil | Statut |
|---|---|---|
| `AT802F_improved.json` | Air Tractor AT-802F Fire Boss | en service |
| `AT802FB_improved.json` | Air Tractor AT-802F Fire Boss | en service |
| `CL215_improved.json` | Canadair CL-215 | retiré |
| `DHC515_improved.json` | De Havilland DHC-515 Firefighter | à l'étude |
| `F100_improved.json` | Hynaero Frégate-F100 | à l'étude |
| `FF72S_improved.json` | Positive Aviation FF72-S | à l'étude |

---

## ⚠ Ce ne sont pas des copies du référentiel

**Ce sont des propositions en attente d'arbitrage.** Leurs valeurs divergent de
celles de `flotte.json`, parfois beaucoup :

| Appareil | Fiche | `flotte.json` actuel |
|---|---|---|
| Air Tractor Fire Boss | **3 103 m** | 1 657 m |
| Canadair CL-215 | **1 500 m** | 1 921 m |
| DHC-515 Firefighter | **1 500 m** | 1 957 m |
| Hynaero Frégate-F100 | **1 984 m** | 1 945 m |
| Positive Aviation FF72-S | **2 212 m** | 2 185 m |

*(longueur d'eau minimale exigée)*

Les deux premiers écarts sont considérables et changent complètement la
géographie de ce que l'appareil peut faire. Ils n'ont **pas** été tranchés.

Deux fichiers portent par ailleurs le **même appareil** — `AT802F` et
`AT802FB`, tous deux le Fire Boss. Lequel fait foi n'est pas établi.

---

## Comment les utiliser

Dans [l'éditeur de flotte](../../../1-outils/ecopage/editeur-flotte.html) :

1. **Chargez d'abord `flotte.json`**, le référentiel complet. Une fiche seule
   remplacerait la flotte entière par un unique appareil.
2. Chargez ensuite la fiche, par *Importer une fiche d'appareil*.
3. L'éditeur détecte que le nom existe déjà et **ouvre une fenêtre
   d'arbitrage** : il liste, champ par champ, l'ancienne valeur et la nouvelle,
   avec leur source respective. Vous choisissez.

Cette fenêtre existe précisément pour ces cas-là : elle empêche qu'un travail
mené à côté écrase silencieusement le référentiel, ou qu'il soit perdu sans
qu'on s'en aperçoive.

Voir la [fiche de l'éditeur](../../../5-documentation/05-editeur-flotte.md).
