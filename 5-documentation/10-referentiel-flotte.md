# Le référentiel de flotte — `flotte.json`

**Fichier** : [`2-donnees/ecopage/flotte.json`](../2-donnees/ecopage/flotte.json)
**Version du schéma** : 6.4
**Contenu** : 14 aéronefs, dont 7 écopeurs dimensionnés

C'est le fichier central du volet écopage. Trois outils le lisent
— plans d'eau, profil de vol, comparatif poids/puissance — et un seul l'écrit :
[l'éditeur de flotte](05-editeur-flotte.md).

---

## Structure générale

```json
{
  "meta":  { ... },
  "fleet": [ { ...appareil... }, ... ]
}
```

La section `meta` documente le fichier lui-même : version, périmètre, date de
mise à jour, et une notice par convention en vigueur — `sourcage`,
`plan_de_vol`, `ecopage`, `longueur_min_m`, `moteur`, `variantes`, `dette`.

**Lisez `meta` avant de modifier quoi que ce soit.** Les conventions y sont
écrites, et elles ne se devinent pas.

---

## La convention de sourçage

C'est ce qui distingue ce référentiel d'une simple table. **Chaque valeur
numérique porte sa provenance.**

```json
"ecopage_vitesse_kmh": 130,
"ecopage_vitesse_kmh_src": "constructeur",
"ecopage_vitesse_kmh_commentaire": "manuel de vol, édition 2019"
```

Le suffixe `_src` puise dans un vocabulaire fermé :

| Valeur | Signification | Statut |
|---|---|---|
| `constructeur` | documentation du constructeur | **trouvée** |
| `publie` | source publique identifiée | **trouvée** |
| `estime` | estimation raisonnée | interprétée |
| `interpole` | déduite d'appareils voisins | interprétée |
| `analogie` | reprise d'un appareil comparable | interprétée |
| `concept` | valeur de projet, appareil non volant | interprétée |
| `calcul` | dérivée d'autres champs par l'outil | interprétée |

Les valeurs interprétées sont marquées d'un astérisque dans les outils.

---

## Les grands blocs de champs

Un appareil porte environ 70 champs de base. Ils se regroupent ainsi :

### Identité

`id`, `name`, `maker`, `makerUrl`, `img`, `firstFlight`, `available`,
`status`, `fin_service`.

`status` vaut `service`, `commande`, `etude`, `concept` ou `retire`. Il
détermine la couleur de l'appareil dans les outils.

### Parc

`qty_n` (nombre exploitable par les calculs), `qty` (affichage), `qtyNote`
(nuance en clair), `ordersFR`, `ordersIntl`, `pilots`, `groundCrew`.

`qty_n` et `qty` coexistent parce que l'affichage veut parfois écrire
« 12 dont 11 disponibles » là où le calcul veut un entier.

### Masse et puissance

`masse_vide_t`, `masse_charge_t`, `puissance_ch`, `moteur_nombre`,
`moteur_ref`. Les champs `emptyMass`, `loadedMass`, `enginePower` sont les
versions texte, destinées à l'affichage.

### Performances

`vitesse_kmh`, `autonomie_km`, `reload`, `runway`. Les doublons `speed`,
`range`, `autonomy`, `speedTxt` sont hérités d'un schéma antérieur et
conservés pour compatibilité.

### Profil de vol d'écopage

C'est le bloc que lit l'outil de profil de vol :

| Champ | Ce qu'il décrit |
|---|---|
| `approche_vitesse_kmh` | vitesse d'approche |
| `approche_angle_nominal_deg` / `_max_deg` | pente de descente |
| `ecopage_vitesse_toucher_kmh` | vitesse au moment du contact |
| `ecopage_duree_avant_s` | durée de la phase **non efficace** avant écopage |
| `ecopage_vitesse_kmh` | vitesse pendant l'écopage efficace |
| `ecopage_duree_efficace_s` | durée de l'écopage **efficace** |
| `ecopage_vitesse_rotation_kmh` | vitesse de rotation en fin de course |
| `decollage_vitesse_kmh` | vitesse de décollage |
| `decollage_angle_nominal_deg` / `_max_deg` | pente de montée |

Le modèle en trois phases est expliqué dans la
[fiche du profil de vol](04-profil-vol-ecopage.md).

### Dimensions d'eau

`citerne_l`, `largeur_min_m`, et surtout **`longueur_min_m`**.

`longueur_min_m` est **entièrement dérivé** : la moyenne entre le cycle le plus
court et le cycle le plus long, tous deux mesurés au seuil pratique de 50 m. Ne
le saisissez jamais à la main — l'éditeur le recalcule.

C'est ce champ qui commande toute la géographie de l'outil des plans d'eau :
il décide quelle eau l'appareil peut utiliser.

### Compatibilités

`mode_recharge`, `compatible_pelicandrome`, `modification_avion_existant`,
`base_cellule_occasion`.

### Économie

`prix_cellule_neuve`, `prix_occasion`, `prix_kit`, `prix_total`,
`quantite_produite_total`, `quantite_en_vol_total`.

Ce sont des champs texte, parce qu'un prix d'acquisition n'a de sens qu'avec sa
date, sa devise et son périmètre — et que les enfermer dans un nombre les
rendrait faussement précis.

---

## Les sept écopeurs dimensionnés

Ceux qui portent un `longueur_min_m` et apparaissent donc sur la carte des
plans d'eau :

| Appareil | Longueur d'eau exigée |
|---|---|
| Salamandre S414 *(concept drone)* | 1 524 m |
| Air Tractor AT-802F Fire Boss | 1 657 m |
| Canadair CL-415 | 1 773 m |
| Canadair CL-215 | 1 921 m |
| Hynaero Frégate-F100 | 1 945 m |
| De Havilland DHC-515 Firefighter | 1 957 m |
| Positive Aviation FF72-S | 2 185 m |

Les sept autres appareils du référentiel n'écopent pas, ou leurs dimensions
d'eau ne sont pas publiées.

---

## La dette documentaire

`meta.dette` recense les champs dont la valeur est encore faible ou dont le
sourçage reste à faire. C'est une liste de travail assumée, pas un oubli.

Deux contradictions de source y sont explicitement laissées à l'arbitrage
humain : `BE200.puissance_ch` et `FF72S.approche_vitesse_kmh`.

---

## Les fiches d'un seul appareil

Le dossier [`2-donnees/ecopage/fiches-appareil/`](../2-donnees/ecopage/fiches-appareil/)
contient six fiches au même schéma, mais ne portant qu'un appareil.

Elles servent à confier l'amélioration d'un appareil à quelqu'un — ou à une IA
— sans lui donner le référentiel entier, puis à réintégrer le résultat.
L'éditeur détecte le nom existant et ouvre une fenêtre d'arbitrage plutôt que
d'écraser. Voir la [fiche de l'éditeur](05-editeur-flotte.md).
