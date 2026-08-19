# Projet « Moyens aériens de lutte contre les feux de forêt »

Manuel de projet. Il décrit le cahier des charges permanent des infographies, l'architecture des données, le dictionnaire des champs, l'état de chaque outil, les faits vérifiés et les pièges déjà rencontrés.

**À lire en entier avant toute modification d'un outil ou d'un fichier de données.** Ce document s'adresse autant à un humain qu'à un agent (Claude, Antigravity, autre) : il tient lieu de spécification. Ce qui y est écrit prime sur ce que fait le code existant, car plusieurs outils sont en retard sur les règles.

Dernière révision : 2026-08-18, à l'issue d'un audit croisé des cinq copies du référentiel de flotte.

---

## 1. Cahier des charges permanent des infographies

Ces règles s'appliquent à **tous** les outils, sans exception. Elles ont été établies au fil du projet et chaque écart a produit un défaut constaté.

### Dimensions et lisibilité

- Zone graphique calibrée sur **1200 px de large**.
- Elle sera **réduite à 800 px par LinkedIn**. Toute police doit rester lisible après cette réduction. En pratique, rien en dessous de 13 px, et 14 à 17 px pour les textes courants.
- **Aucun ascenseur horizontal** dans la zone destinée à la capture. Le défilement est toléré uniquement dans un conteneur de tableau isolé, jamais sur la page.
- La hauteur est libre. Mieux vaut allonger que comprimer.
- Les **paramètres se placent hors de la zone de capture**, en dessous, avec une séparation visuelle nette.

### Rendu

- Fond sombre (`--bg: #0f172a`), cartes `#1e293b`, bordures `#334155`, accent `#38bdf8`.
- Design plat, minimaliste, pas d'ombres ni de dégradés décoratifs.
- Pas d'icônes ni d'émojis dans les graphiques.
- Les légendes se placent **sous** le graphique, sur toute la largeur, jamais dans une colonne latérale étroite.

### Autonomie technique, règle absolue

- **Aucune dépendance chargée depuis un CDN, quel qu'il soit.** D3 (environ 280 Ko) et html2canvas (environ 200 Ko) s'embarquent dans le fichier.
  Motif : `d3js.org` et `cdn.jsdelivr.net` sont bloqués dans certains environnements, ce qui a produit deux pages entièrement blanches sans le moindre message d'erreur. `cdnjs.cloudflare.com` n'a pas encore échoué, mais il n'offre aucune garantie de plus : **arbitrage du 2026-08-18, aucune liste blanche, on embarque tout.**
- Les **fonds de carte GeoJSON sont embarqués**, jamais chargés à distance.
- Tout script doit être **enveloppé dans un `try/catch`** qui affiche l'erreur en rouge en haut de page. Une page blanche silencieuse est le pire des échecs.
- Les `<svg>` portent des attributs `width` et `height` **explicites**, en plus du `viewBox`. Sans quoi ils font 0×0 si le script échoue.
- `ResizeObserver` doit être gardé : `if (typeof ResizeObserver !== "undefined")`. Sinon le script casse dans certains environnements.

### Captures d'écran

L'implémentation de référence est la fonction `capture()` de `distance_pelicandrome_v11_1.html`. Tout nouvel outil la reprend telle quelle.

- Marge de **10 px sur les quatre côtés**, posée sur l'élément avant la capture (`el.style.padding='10px'`) et **retirée après**, valeur précédente restaurée.
- Nom de fichier **préfixé par le sujet** (appareil sélectionné, région, nombre d'appareils). Jamais de nom fixe.
- Les images distantes sont **converties en data-URI avant la capture**, puis les `src` d'origine sont restaurés.
- Si une image ne peut pas être convertie, **avertissement nommant les images concernées, avec possibilité d'annuler**, avant que la capture ne parte.
- Sur les images distantes : ne **jamais** poser `crossorigin="anonymous"` sur une balise `<img>`. Cet attribut force une requête CORS et fait échouer l'affichage chez la majorité des hébergeurs. Utiliser `referrerpolicy="no-referrer"` seul, avec un `onerror` qui affiche la cause.
- Conséquence : une image affichée sans CORS ne peut pas être peinte par html2canvas. Deux parades, à proposer à l'utilisateur : importer le fichier depuis le disque (converti en data-URI, toujours capturable), ou l'héberger sur `raw.githubusercontent.com`, qui envoie `Access-Control-Allow-Origin: *`.
- Un **badge de diagnostic** par image, calculé sans attendre la capture : intégrée / capturable / affichable mais non capturable / introuvable.

### Interaction

- Les modales d'**édition** ne se ferment pas au clic extérieur. On perd la saisie. Seuls Annuler et Valider ferment.
- Les modales purement informatives peuvent se fermer au clic extérieur.
- Les messages de suppression doivent dire la vérité sur la persistance : rien n'est définitif tant que le JSON n'a pas été réexporté.

---

## 2. Règles éditoriales pour les articles

- Écriture à la première personne, registre engagé mais informé, phrases courtes.
- **Pas de tirets longs.** Préférer les parenthèses, les virgules, les points.
- Pas d'icônes, pas de structure de liste typique des IA.
- Sur LinkedIn : un émoji en tête, un au pivot, un en fin. Puces au triangle `▸`.
- Le gras LinkedIn passe par le bloc Unicode « Mathematical Sans-Serif Bold ». Le `é` n'existe pas dans ce bloc : utiliser `𝗲` suivi de l'accent combinant U+0301. Réserve : les lecteurs d'écran ne lisent pas ces caractères, et la recherche ne les indexe pas. Garder au moins une occurrence en caractères normaux.
- Toute erreur factuelle doit être **signalée avant** correction. Les corrections importantes se valident avec l'utilisateur.

---

## 3. Architecture des données

C'est la partie que tout agent doit avoir lue avant de toucher au moindre fichier.

### 3.1 Principe général

Un fichier de données par domaine, et **un seul**. Les outils n'inventent pas de schéma local.

| Fichier | Domaine | Clé racine |
|---|---|---|
| `flotte.json` | Les aéronefs, et rien d'autre | `fleet[]` |
| `chronologie-pelicandromes_4_1.json` | Le réseau au sol : position, statut, historique daté | `sites.<id>` |
| `plans-eau-france.json` | Les axes d'écopage mesurés | `axes[]` |
| `profils-vol-ecopage-v19.json` | Réglages d'**affichage** du profil de vol | `profils[]`, `glob`, `actif` |
| `parametres-utilisateur-pelicandromes.json` | Réglages d'interface, partagés entre outils | voir 4.4 |
| `carte2-data-v2.json` | Couleurs de la carte fréquence | clé 2 car. = département, 5 car. = arrondissement |

**Séparation des responsabilités, à respecter :**

- `flotte.json` ne contient **que** les aéronefs. Aucune position, aucun statut de station.
- `chronologie-*.json` porte **l'intégralité** du réseau au sol.
- Ajouter un pélicandrome se fait dans la chronologie **seule**.
- Historique : jusqu'en v3, la flotte portait aussi le réseau, parce que seul l'outil Distance Pélicandrome avait une fonction d'ajout manuel d'aérodrome et que son export sérialisait tout. Corrigé en v4.

### 3.2 Le référentiel de flotte

Structure : `{ "meta": {...}, "fleet": [ ... ] }`, sérialisé avec **un espace d'indentation** (`JSON.stringify(DATA, null, 1)`).

Chaque entrée de `fleet[]` est un objet plat. Pas d'imbrication.

**Nom de fichier canonique : `flotte.json`.** Les noms `flotte-pelicandromes.json`, `flotte-pelicandromes_4.json` et `flotte (1).json` sont des reliquats à ne plus produire.

### 3.3 Règle d'écriture du référentiel

Arbitrage du 2026-08-18. **Tout outil peut exporter la flotte**, à trois conditions strictes :

1. Il exporte sous le nom **`flotte.json`**, jamais sous un autre.
2. Il **conserve le bloc `meta` reçu à l'import**, en totalité. Il n'a pas le droit de le remplacer par un meta de son cru.
3. Il n'ajoute qu'**une ligne d'horodatage**, dans `meta.derniere_maj`, au format `AAAA-MM-JJ — <ce qui a été fait>`.

Un outil qui ne connaît pas tout le schéma **ne doit pas perdre les champs qu'il ignore** : il les recopie tels quels. L'éditeur de flotte montre la marche à suivre, il affiche les champs hors schéma dans une section « Champs hors schéma (conservés tels quels) » plutôt que de les jeter.

Violations constatées au 2026-08-18, à corriger : `plans-eau-ecopage.html` écrit un `meta` maison `version: 3` et ne connaît que 33 champs sur 113 ; `distance_pelicandrome_v11_1.html` écrit un `meta` codé en dur `2026-07-23-v4` ; `profil-vol-ecopage-v18.html` exporte sous `flotte-pelicandromes.json`.

### 3.4 Convention de sourçage

C'est le cœur de la v6. **Toute grandeur numérique exploitée par un algorithme existe en trois champs frères :**

| Champ | Contenu |
|---|---|
| `<champ>` | La valeur brute, **numérique**. Jamais de texte, jamais d'unité, jamais d'espace insécable. |
| `<champ>_src` | Le statut de la source, dans un vocabulaire fermé (ci-dessous). |
| `<champ>_commentaire` | L'URL de la source, **ou** la base du raisonnement si la valeur est interprétée. |

Vocabulaire fermé de `_src` :

| Valeur | Sens | Affichage |
|---|---|---|
| `""` | non renseigné | « ? » |
| `constructeur` | fiche ou manuel du constructeur | donnée **trouvée** |
| `publie` | source publique tierce sérieuse | donnée **trouvée** |
| `estime` | estimation raisonnée | donnée **interprétée**, astérisque |
| `interpole` | interpolée entre deux valeurs connues | interprétée, astérisque |
| `analogie` | reprise d'un appareil comparable | interprétée, astérisque |
| `concept` | valeur de conception, non volante | interprétée, astérisque |
| `calcul` | **dérivée** par le bloc de calcul partagé, jamais saisie | interprétée, astérisque |

`constructeur` et `publie` valent « trouvée » (vert). Tout le reste vaut « interprétée » (jaune, astérisque). C'est la fonction `TROUVE()` de l'éditeur.

**Les outils tirent leurs légendes de ces commentaires. Aucune référence n'est codée en dur dans un outil.** Le motif d'affichage de référence, dans `distance_pelicandrome_v11_1.html` :

```
['Capacité citerne', `${f.citerne_l||'—'} L <span grisé>${f.citerne_commentaire||''}</span>`]
```

Nomenclature du commentaire, **arbitrage du 2026-08-18** : la forme canonique est `<champ>_commentaire`, c'est-à-dire construite sur le nom **complet** du champ, unité comprise. `vitesse_kmh_commentaire`, pas `vitesse_commentaire`.

> Dette à résorber. Quatre commentaires historiques portent encore un nom tronqué et contiennent le texte, tandis que leur homologue canonique existe mais est **vide** : `vitesse_commentaire` → `vitesse_kmh_commentaire`, `autonomie_commentaire` → `autonomie_km_commentaire`, `citerne_commentaire` → `citerne_l_commentaire`, et `ecopage_commentaire` qui sert pour **deux** champs, `longueur_min_m_commentaire` et `largeur_min_m_commentaire`. Tant que la migration n'est pas faite, **un agent qui lit la forme canonique obtient une chaîne vide**. Lire les deux, préférer le non-vide.

### 3.5 Dictionnaire des champs de `fleet[]`

Colonne « src » : le champ porte `_src` et `_commentaire`.

**Identité**

| Champ | Type | src | Remarque |
|---|---|---|---|
| `id` | texte | | Clé de liaison entre outils. Immuable. |
| `name` | texte | | Nom affiché. Ne sert **pas** de clé (voir 3.7). |
| `maker`, `makerUrl` | texte | | |
| `img` | texte | | URL ou data-URI. Voir les règles de capture. |
| `firstFlight`, `available` | texte | | Libre. |
| `status` | énum | | `service` \| `commande` \| `etude` \| `concept` \| `retire` |
| `fin_service` | entier ou `null` | oui | Année. `null` = aucune date connue. **Le seul champ numérique qui reste à `null` au lieu d'être supprimé quand il est vide.** |

**Flotte française**

| Champ | Type | src | Remarque |
|---|---|---|---|
| `qty_n` | entier | | Quantité exploitable par un algorithme. `0` pour les projets et pour les flottes non détenues. *À créer, décision du 2026-08-18.* |
| `qty` | texte | | Quantité affichée telle quelle : « 12 », « Variable », « 4 commandés », « 0 dédié ». **Aucun outil ne doit tenter de la parser.** |
| `qtyNote` | texte | | Précision. |
| `ordersFR`, `ordersIntl`, `pilots`, `groundCrew` | texte | | |

**Masses et puissance**

| Champ | Type | src | Remarque |
|---|---|---|---|
| `masse_vide_t` | nombre | oui | Tonnes. Séparateur décimal **point**, jamais virgule. |
| `masse_charge_t` | nombre | oui | Tonnes. Pour un amphibie, c'est la masse **au décollage après écopage**, pas la MTOW terrestre. Voir le CL-415 : 21,32 t et non 19,89 t. |
| `puissance_ch` | entier | oui | Puissance **totale**, tous moteurs. |
| `moteur_nombre` | entier | oui | Nombre de moteurs. |
| `moteur_reference` | texte | oui | Référence du moteur, seule : « Pratt & Whitney Canada PW123AF ». Ni le nombre, ni la puissance, ni de commentaire. |
| `moteur_puissance_unitaire_ch` | nombre | | **Calculé** : `puissance_ch / moteur_nombre`. |
| `enginePower` | texte | | **Calculé** : `<nombre> × <unitaire> ch (<référence>)`. |
| `emptyMass`, `loadedMass` | texte | | Formes affichées, héritées v5. Réalignées sur les valeurs numériques. |
| `enginePowerSrc` | texte | | Champ de source historique v5, hors convention. Conservé. |

> **Le champ moteur a été éclaté le 2026-08-18.** `enginePower` était une chaîne unique qui mélangeait le nombre de moteurs, la puissance unitaire, la référence et parfois un commentaire : rien n'y était interrogeable, et le texte pouvait contredire `puissance_ch` sans que personne le voie. La nuance qui traînait en fin de chaîne (« version pompier Conair », « moteurs à pistons ») est passée dans `moteur_reference_commentaire`.

**Performances**

| Champ | Type | src | Remarque |
|---|---|---|---|
| `vitesse_kmh` | entier | oui | Vitesse de croisière. |
| `autonomie_km` | entier | oui | Distance franchissable totale. |
| `reload` | entier | oui | Rechargement au pélicandrome, minutes. `0` si sans objet. |
| `runway` | texte | | Piste requise, forme affichée. |

**Plan de vol** — le référentiel du profil d'écopage. Tous portent `_src` et `_commentaire`. Le mode d'emploi complet est en **3.5 bis**, à lire avant de renseigner une fiche.

| Champ | Unité | Ce qu'il dessine |
|---|---|---|
| `approche_vitesse_kmh` | km/h | Étiquette de la branche d'approche. |
| `approche_angle_nominal_deg` | ° | Pente du trait vert plein. Plan de descente standard. |
| `approche_angle_max_deg` | ° | Pente du trait vert pointillé. Approche sous contrainte (canyon, ravine). |
| `ecopage_vitesse_kmh` | km/h | Vitesse de la phase **efficace** seule. |
| `ecopage_vitesse_toucher_kmh` | km/h | Vitesse au contact de l'eau, début du segment d'entrée. |
| `ecopage_vitesse_rotation_kmh` | km/h | Vitesse d'arrachement, fin du segment de sortie. |
| `ecopage_duree_avant_s` / `ecopage_distance_avant_m` | s / m | Segment sombre d'entrée. Saisir l'un, l'autre se calcule. |
| `ecopage_duree_efficace_s` / `ecopage_distance_efficace_m` | s / m | Segment bleu clair, le remplissage continu. Saisir l'un, l'autre se calcule. |
| `ecopage_duree_apres_s` / `ecopage_distance_apres_m` | s / m | Segment sombre de sortie. Saisir l'un, l'autre se calcule. |
| `ecopage_duree_s` | s | **Calculé.** Durée de contact totale, les trois phases. |
| `ecopage_distance_m` | m | **Calculé.** Longueur totale de la barre bleue au niveau de l'eau. |
| `longueur_min_m` | m | **Calculé.** Longueur de plan d'eau de référence, formule ci-dessous. |
| `decollage_vitesse_kmh` | km/h | Étiquette de la branche de montée. |
| `decollage_angle_nominal_deg` | ° | Pente du trait orange plein. |
| `decollage_angle_max_deg` | ° | Pente du trait orange pointillé. Évitement d'obstacle. |

### 3.5 bis Comment renseigner un profil d'écopage

**C'est la section à lire avant de toucher aux champs `ecopage_*`.** Elle décrit ce que l'outil calcule, donc ce qu'il attend.

**La course sur l'eau se décompose en trois phases, dans cet ordre :**

```
   toucher de l'eau                                        arrachement
        |                                                       |
        |<-- 1. entrée -->|<-- 2. efficace -->|<-- 3. sortie -->|
        |   non efficace  |   la citerne se   |  non efficace   |
        |                 |     remplit       |                 |
   vTouche ---------> vEco ============= vEco ---------> vRotation
        |   tAvant        |      tEff         |    tApres       |
```

| Phase | Durée | Vitesses | Champ JSON |
|---|---|---|---|
| 1. Entrée, roulage non efficace | `ecopage_duree_avant_s` | de `ecopage_vitesse_toucher_kmh` à `ecopage_vitesse_kmh` | à renseigner |
| 2. Écopage efficace | `ecopage_duree_efficace_s` | `ecopage_vitesse_kmh`, constante | à renseigner |
| 3. Sortie, déjaugeage plein | **déduite**, jamais saisie | de `ecopage_vitesse_kmh` à `ecopage_vitesse_rotation_kmh` | aucun |

La phase 3 se déduit : `tApres = ecopage_duree_s − ecopage_duree_efficace_s − ecopage_duree_avant_s`. **Il n'existe pas de champ pour elle.** Pour l'allonger ou la raccourcir, on agit sur `ecopage_duree_s`.

**Chaque distance suit un profil trapézoïdal**, la vitesse variant linéairement dans les phases 1 et 3 :

```
dAvant = (vTouche + vEco) / 2 × tAvant
dEff   =            vEco      × tEff
dApres = (vEco + vRotation) / 2 × tApres
dTotal = dAvant + dEff + dApres
tTotal = tAvant + tEff + tApres
```

### Ce qui se saisit, ce qui se calcule

**Aucun agent, humain ou non, ne pose un chiffre calculable.** C'est la règle qui gouverne toute cette section. Un calcul refait à la main est un calcul qui divergera d'un outil à l'autre.

| | Champs | Qui les remplit |
|---|---|---|
| **Saisi** | les trois vitesses, et **par phase la durée OU la distance** | l'humain, d'après une source |
| **Calculé** | l'autre membre de chaque paire durée/distance, `ecopage_duree_s`, `ecopage_distance_m`, `longueur_min_m` | le bloc de calcul partagé, à chaque chargement |

Les champs calculés portent `_src` = **`calcul`**. Dans l'éditeur de flotte ils s'affichent grisés et non modifiables. Les écraser à la main ne sert à rien : ils sont recalculés à l'ouverture suivante.

**Pourquoi une paire durée/distance par phase.** Les documentations constructeur donnent tantôt l'une, tantôt l'autre. Le CL-415 est publié à « 410 à 450 m » (une distance) et à « 12 secondes » (une durée) ; le Fire Boss uniquement en secondes. On saisit ce qui est publié, la machine déduit le reste par `d = v × t`. Renseigner les deux membres d'une paire est permis mais inutile : le bloc n'écrase jamais une valeur posée, et un désaccord entre les deux ne serait pas signalé.

**Piège documenté, celui qui a produit un écart de 38 % sur le CL-415.** Les 410 à 450 m publiés décrivent la **phase efficace**, celle des 12 secondes de remplissage. Le contact total, entrée et sortie comprises, fait 594 m. Confondre les deux met une durée totale en face d'une distance efficace, et rien ne tient. C'est précisément pour rendre cette confusion impossible que la distance efficace a désormais son propre champ.

**Ordre de renseignement recommandé :**

1. `ecopage_vitesse_kmh`, plus `ecopage_duree_efficace_s` **ou** `ecopage_distance_efficace_m` : ce sont les seules grandeurs que les constructeurs publient. Si la vitesse est inconnue, poser la durée **et** la distance suffit : la vitesse s'en déduit.
2. `ecopage_vitesse_toucher_kmh` et `ecopage_vitesse_rotation_kmh` : à défaut de source, appliquer la convention du projet, calée sur le CL-415, **en marquant `_src` à `analogie`** :
   `vTouche = 1,115 × vEco` et `vRotation = 1,285 × vEco`.
3. `ecopage_duree_avant_s` : 1 à 1,5 s selon la masse (1 s sous 10 t, 1,5 s au-delà).
4. `ecopage_duree_apres_s` : 2 s pour un appareil léger, 2,5 s pour un Canadair, 3 s au-dessus de 25 t.
5. `decollage_vitesse_kmh` : au moins égal à `ecopage_vitesse_rotation_kmh`. Convention du projet : `1,108 ×`.
6. Ne rien saisir d'autre. Les totaux et la longueur de plan d'eau apparaissent seuls.

### La longueur de plan d'eau est une grandeur formelle

`longueur_min_m` n'est **pas** une donnée sourcée. Les publications sont trop dispersées pour servir de référence partagée : 1 340 m, 1 500 m et 2 000 m circulent pour le seul CL-415, selon qu'on mesure la course sur l'eau, la manœuvre d'un seuil de 15 m à l'autre, ou l'axe jugé confortable par un équipage.

Le projet en fait donc une **convention de calcul**, identique pour tous les appareils, arrêtée le 2026-08-18 :

> `longueur_min_m` = moyenne entre le **cycle le plus court** et le **cycle le plus long**, mesurés d'un **seuil de 50 m** à l'autre.
>
> ```
> court = 50/tan(approche_angle_max)     + dTotal + 50/tan(decollage_angle_max)
> long  = 50/tan(approche_angle_nominal) + dTotal + 50/tan(decollage_angle_nominal)
> longueur_min_m = (court + long) / 2
> ```

Le seuil de 50 m est celui que le profil de vol appelle « seuil pratique ». Il ne vient d'aucun règlement : c'est une hauteur de franchissement d'obstacle raisonnable, choisie pour être la même partout. Les angles maximaux donnent les pentes les plus fortes, donc le cycle le plus court.

**Conséquence à connaître avant d'interpréter un chiffre.** À 3°, la seule descente depuis 50 m occupe déjà 954 m. Les branches d'approche et de montée pèsent donc **deux à trois fois plus lourd que la course sur l'eau**, et le classement des appareils se joue davantage sur leurs angles que sur leur performance d'écopage. Un appareil qui écope court mais monte doucement peut exiger un plan d'eau plus long qu'un Canadair. Le tableau des valeurs obtenues et de leur effet sur la couverture est en 10.

**Où le calcul a lieu, exactement.** La valeur existe à trois endroits, et ils sont tenus d'être d'accord :

| Où | Quoi | Quand |
|---|---|---|
| `flotte.json` | `longueur_min_m` avec `_src: "calcul"` | écrit à l'export, lisible hors de tout outil |
| Bloc de calcul partagé, dans les 4 outils | `ECO.planEau(fiche)` | **recalculé à chaque chargement**, à chaque import, à chaque validation de fiche |
| `profil-vol`, fonction `planEauProfil()` | même formule, sur la géométrie **affichée** | à chaque rendu |

La valeur stockée dans le JSON ne peut donc jamais être obsolète : un outil qui l'ouvre la recalcule avant de s'en servir. Elle y figure quand même, pour qu'un agent ou un tableur qui lit le fichier seul y trouve le chiffre.

La seule différence entre les deux derniers : le bloc partagé lit les angles de la **fiche de flotte**, `planEauProfil()` lit ceux du **profil affiché**. Les deux coïncident tant que le profil n'a pas été surchargé à la main, la flotte faisant foi. Si l'utilisateur déplace un angle pour composer son infographie, le nombre du bandeau suit le dessin : c'est voulu, une infographie doit dire ce qu'elle montre.

**Affichage.** Le profil de vol porte la valeur **en turquoise, à droite du nom de l'appareil**, dans le bandeau de titre : c'est la grandeur qui décide de tout en aval, elle ne doit pas se chercher. Elle est par construction la médiane des deux bornes de la barre violette « Cycle complet au seuil 50 m ».

**Contrôles de vraisemblance à passer avant de valider une fiche :**

- `ecopage_duree_efficace_s` ≤ `ecopage_duree_s`
- `ecopage_vitesse_toucher_kmh` ≥ `ecopage_vitesse_kmh` et `ecopage_vitesse_rotation_kmh` ≥ `ecopage_vitesse_kmh`
- `decollage_vitesse_kmh` ≥ `ecopage_vitesse_rotation_kmh`
- `ecopage_distance_m` ≤ `longueur_min_m` : la course doit tenir dans le plan d'eau minimal annoncé
- débit `citerne_l / ecopage_duree_efficace_s` : 511 L/s sur le CL-415. Très au-delà, la valeur est un chiffre de communication, pas une performance.

**Réglage de l'outil.** Le sélecteur « Valeur calculée par règle de trois » doit être sur **« aucune »** dès que les trois phases sont renseignées. Les autres réglages imposent `d = v × t`, ce qui est faux ici puisque l'entrée et la sortie se font à d'autres vitesses. La reprise depuis la flotte le positionne toute seule.

**Écopage et emport**

| Champ | Type | src | Remarque |
|---|---|---|---|
| `citerne_l` | entier | oui | Volume d'**eau larguée**, en litres. Un additif éventuel se décrit dans le commentaire, il ne s'additionne pas à la valeur. |
| `mode_recharge` | booléen | | `true` = écopage sur plan d'eau **et** pélicandrome. `false` = pélicandrome exclusivement. Libellé fixe côté outil, jamais du texte libre. |
| `compatible_pelicandrome` | booléen | | |
| `longueur_min_m` | entier | oui | Plan d'eau minimal. Renseigné **si et seulement si** `mode_recharge` est vrai. |
| `largeur_min_m` | entier | oui | Idem. |
| `tank`, `scoop` | texte | | Formes affichées, héritées. |

**Prix et production** — tous en texte libre, aucun n'est calculé.

`modification_avion_existant` (booléen), `base_cellule_occasion` (booléen), `prix_cellule_neuve`, `prix_occasion`, `prix_kit`, `prix_total`, `quantite_produite_total`, `quantite_en_vol_total`, `cadence_production_avion`, `cadence_production_kit`.

`prix_kit` et `cadence_production_kit` **ne s'affichent que si `modification_avion_existant` est vrai**.

**Divers**

| Champ | Type | Remarque |
|---|---|---|
| `speed` | entier | **Miroir** de `vitesse_kmh`, réécrit à chaque validation de l'éditeur. Ne jamais le modifier à la main. |
| `range` | entier | **Miroir** de `autonomie_km`, idem. |
| `autonomy`, `speedTxt`, `rotationRange` | texte | Formes affichées héritées. |
| `comment` | texte long | Commentaire éditorial de l'appareil. |
| `verif` | texte long | Bilan de fiabilité : ce qui a été vérifié, ce qui ne l'a pas été, avec les sources. |

### 3.6 Valeurs dérivées, jamais stockées

Ces grandeurs se **calculent** à l'affichage. Les stocker, c'est garantir qu'elles divergeront.

| Grandeur | Calcul | Mention à afficher |
|---|---|---|
| Autonomie de rotation | `autonomie_km / 2` | « moitié de la distance franchissable, l'appareil devant revenir » |
| Durée max de rotation | `8 + 8 + reload + 2 × ((autonomie_km/2) × 1,05 / vitesse_kmh) × 60` | « calculée depuis l'autonomie et la vitesse » |
| Statut effectif | `fin_service ≤ année courante → retire` | |
| Cycle d'écopage | `manœuvre_écopage + manœuvre_largage + 2 × (dist × 1,05 / vitesse_kmh) × 60` | L'écopeur **ne se pose pas** : pas de décollage ni d'atterrissage dans le cycle. |

Constantes partagées : `TIME_TAKEOFF = 8`, `TIME_LANDING = 8` (minutes, rotation au sol seulement), `CONST_DIST_FACTOR = 1,05` (sinuosité de la route), `EARTH_R = 6371` km.

### 3.7 Variantes d'appareil

**Arbitrage du 2026-08-18 : une ligne de flotte par variante.**

Motif : la capacité d'écopage est une propriété de la **variante**, pas de la famille. Confondre les deux a produit deux incohérences réelles dans le référentiel actuel :

- `AT802` porte le nom « Air Tractor AT-802F Fire Boss » et `mode_recharge: true`, alors que le Fire Boss est la version amphibie à flotteurs, **absente de France**, et que l'AT-802F terrestre n'écope pas.
- `FF72` porte un profil de vol d'écopage complet mais `mode_recharge: false`, `citerne_l: 0` et aucune dimension de plan d'eau. Le fichier de profils désigne un « Positive Aviation FF72-**S** », visiblement la variante amphibie.

Règle : chaque variante reçoit son propre `id` (`AT802` et `AT802FB`, `FF72` et `FF72S`), son propre `mode_recharge`, sa propre citerne et son propre plan de vol. Le lien de parenté se dit dans `comment`.

Corollaire : `id` est la seule clé de liaison. **Aucun outil ne doit lier par `name`.** La table `CORRESP` de `profil-vol-ecopage-v18.html`, qui fait correspondre un nom de profil à un identifiant de flotte, est une béquille à supprimer.

### 3.8 Autorité entre la flotte et les profils de vol

**Arbitrage du 2026-08-18 : la flotte fait foi, le profil affiche.** Appliqué.

- `flotte.json` porte les **valeurs** de plan de vol, avec leur sourçage.
- `profils-vol-ecopage-v19.json` ne porte que l'**affichage** : mise en page, couleurs, unités, légendes fléchées, barres, animation, échelles.
- La correspondance entre les deux modèles est **entièrement décrite par la table `PLANVOL`** de `profil-vol-ecopage-v18.html` : quinze lignes `[champ de flotte, chemin dans le profil, clé de source, conversion]`. C'est le seul endroit à corriger quand le schéma bouge.
- Le vocabulaire de source à sept valeurs de la flotte se réduit au booléen du profil par la même règle que partout : `constructeur` et `publie` donnent « donnée constructeur », tout le reste « valeur estimée ».
- Les vitesses sont en **km/h dans la flotte** et en **m/s dans le profil**. La conversion est portée par `PLANVOL`, nulle part ailleurs.

**Quand la reprise a lieu :**

| Moment | Portée |
|---|---|
| Ouverture de l'outil | Le profil actif **et** toute la bibliothèque |
| Import d'un JSON de flotte | Tous les profils reliés, avec le compte dans le message |
| Bouton « Reprendre les valeurs de vol depuis la flotte » | Le profil actif, après confirmation listant les champs concernés |

Entre deux reprises, une valeur saisie à la main reste en place : c'est une surcharge locale, et un bandeau permanent indique en jaune quelles valeurs s'écartent de la fiche. **Une modification faite dans le profil ne remonte jamais dans la flotte.** Pour la rendre durable, il faut éditer la fiche puis réexporter le JSON.

La liaison se fait par `id`, via la table `CORRESP` qui traduit le nom du profil en identifiant de flotte. Un profil sans correspondance est signalé en jaune et garde ses propres valeurs : c'est le cas du Beriev Be-200 Altair, absent de la flotte française.

---

## 4. Les autres fichiers de données

### 4.1 Chronologie des pélicandromes

`chronologie-pelicandromes_4_1.json`, clé `sites.<id>`. 33 sites : position, type, date de création, changements de statut datés, sources. C'est le **seul** porteur du réseau au sol.

### 4.2 Plans d'eau

`plans-eau-france.json`, clé `axes[]`. 1 731 axes dédoublonnés sur 96 départements, plus les adjacences. Les 22 `axes-ecopage-<région>.geojson` sont les fichiers régionaux bruts, 1 915 axes avant dédoublonnage.

Le fichier porte aussi `adjacences`, la table des départements limitrophes (96 clés), et un `meta` qui rappelle la méthode et les limites.

**93 départements portent au moins un axe**, sur les 96 clés de la table d'adjacence. Les versions antérieures de ce document annonçaient 96 départements : c'était le compte des adjacences, pas celui des départements pourvus.

Ce fichier a été réextrait des données embarquées de `plans-eau-ecopage.html` le 2026-08-18, et l'extraction a été vérifiée fidèle axe par axe. Il redevient la source, l'outil n'en portant plus qu'une copie.

Structure d'un axe, telle que la lisent les outils : `n` (nom), `l` (longueur en m), `ha` (aire en hectares), `d` (département), `a` et `b` (extrémités, `[lon, lat]`).

Les outils acceptent aussi le GeoJSON, avec la correspondance `properties.nom → n`, `longueur_m → l`, `aire_ha → ha`, `departement → d`, première et dernière coordonnée → `a` et `b`.

### 4.3 Profils de vol

`profils-vol-ecopage-v19.json` : `meta`, `actif` (le profil courant), `profils[]` (la bibliothèque), `glob` (les réglages communs).

Apport de la v19 : les réglages communs (mise en page, couleurs, unités, teinte de roulage) sont **extraits dans `glob`** et sérialisés une seule fois. Les copies par profil sont conservées pour les anciens outils mais **ignorées au chargement**.

### 4.4 Paramètres utilisateur

`parametres-utilisateur-pelicandromes.json`. **Convention de nommage à respecter absolument**, elle évite les effets de bord entre outils :

- **À la racine**, uniquement les clés **partagées** : `labelPositions`, `colors`, `fontSize`, plus `version`, `genere`, `outil`, `_note`.
- **Sous une clé au nom de l'outil**, tout le reste : `distancePelicandrome: { ... }`. Les autres outils ignorent cette clé.
- Un outil qui gagne des réglages ajoute **sa propre clé** (`plansEau`, `profilVol`), il ne pollue pas la racine.
- L'import est tolérant : une clé absente laisse la valeur en place, elle ne la remet pas à zéro.

Exception documentée : l'état coché/décoché des **familles** de sites (`hiddenTypes`, `noCircleTypes`) n'est ni sauvegardé ni rechargé, à la demande de l'utilisateur, pour que les défauts se réappliquent à chaque ouverture. Le fichier porte cette explication dans `_note`.

Règle générale : **tout réglage utilisateur doit être exportable et réimportable en JSON.**

### 4.5 Données embarquées dans les outils

Les JSON de référence sont **embarqués en dur** dans chaque outil, dans un bloc encadré par des bandeaux de commentaire, avec la correspondance fichier ↔ constante indiquée :

```html
<!-- ===== BLOC DE DONNÉES EMBARQUÉES — DÉBUT =====
     data-flotte  <-> flotte.json (v6, commun à tous les outils)
     data-profils <-> profils-vol-ecopage-v19.json (bibliothèque d'usine) -->
<script id="data-flotte" type="application/json"> … </script>
<!-- ===== BLOC DE DONNÉES EMBARQUÉES — FIN ===== -->
```

Les boutons d'import restent disponibles et écrasent ces valeurs à chaud.

### 4.6 Le bloc de calcul partagé

Un second bloc, **identique dans les quatre outils**, porte les calculs d'écopage :

```html
<!-- ===== BLOC DE CALCUL PARTAGE — ECOPAGE : DEBUT ===== -->
<script> var ECO = (function(){ ... })(); </script>
<!-- ===== BLOC DE CALCUL PARTAGE — ECOPAGE : FIN ===== -->
```

Il expose quatre fonctions :

| Fonction | Rôle |
|---|---|
| `ECO.completer(fiche)` | Remplit les trous : l'autre membre de chaque paire durée/distance, les totaux, `longueur_min_m`. **N'écrase jamais une valeur posée.** Renvoie la liste des champs déduits. |
| `ECO.cycle(fiche, h)` | Cycle complet d'un seuil `h` à l'autre : `{court, lng, moyenne}`. |
| `ECO.planEau(fiche)` | `cycle(fiche, 50).moyenne`, la longueur de plan d'eau de référence. |
| `ECO.ecart(fiche)` | Écart entre la course totale enregistrée et la somme des phases. Doit valoir zéro. |

**Règles d'usage, à respecter dans tout nouvel outil :**

- appeler `ECO.completer()` sur **chaque fiche** juste après le chargement du bloc embarqué, et de nouveau après chaque import de flotte ou chaque validation d'édition ;
- ne jamais recopier la formule ailleurs. Un outil qui recalcule à sa façon finira par diverger ;
- le bloc se met à jour par un script d'injection qui réécrit les quatre copies d'un coup et vérifie ensuite qu'elles sont identiques. **Ne jamais modifier une copie isolément.**

**Le bloc embarqué se resynchronise à chaque évolution du référentiel.** Un outil dont le bloc est en retard fonctionne parfaitement et affiche des chiffres périmés, sans le moindre signal : c'est le mode de défaillance le plus coûteux du projet.

---

## 5. Conventions d'interface partagées

L'implémentation de référence est `distance_pelicandrome_v11_1.html`. Tout nouvel outil s'y aligne.

### Carte d'identité d'appareil

- Cadre coloré par statut : vert `service`, orange `etude` et `commande`, violet `concept`, gris `retire`. **Les cinq statuts, pas trois.**
- Bandeau supérieur avec le nom et des pastilles : statut, Écopage, Pélicandrome.
- Photo en `<img referrerpolicy="no-referrer">` avec `onerror` explicite, jamais en fond CSS.
- Chaque ligne affiche **la valeur puis son commentaire en gris**, tiré du JSON.
- Les booléens s'affichent avec un **libellé fixe**, identique d'un appareil à l'autre : « Compatible écopage sur plan d'eau et pélicandrome » / « Pélicandrome exclusivement ». C'est un binaire, pas du texte libre.
- Les lignes conditionnelles n'apparaissent que si elles ont un sens (`prix_kit` seulement pour une conversion).
- Une ligne « Fiabilité » ferme la fiche, reprenant `verif`.

### Sélection d'appareils

Combo à cases multiples, chaque ligne portant une pastille de statut et, à droite, la contrainte d'écopage (`longueur_min_m` en mètres, ou « sol »). Double-clic sur une fiche pour éditer.

### Import d'une fiche d'appareil isolée

L'éditeur de flotte accepte, en plus du référentiel complet, le **JSON d'un seul appareil**. Le cas d'usage est celui d'une recherche menée appareil par appareil, dont le résultat doit rejoindre le fichier commun.

Trois formes sont acceptées : la fiche nue, un tableau d'une fiche, ou `{meta, fleet:[une fiche]}`. L'appareil cible est reconnu par `id`, à défaut par `name` — un nom strictement identique suffit. S'il n'existe pas, la fiche est créée, mais **elle n'entre dans la flotte qu'à la validation** : annuler ne laisse rien derrière.

**Règle absolue : rien n'est appliqué sans arbitrage.** La fenêtre liste **tout ce qui diffère**, et pour chaque ligne affiche des deux côtés la valeur, son statut de source et son commentaire. Une valeur importée n'est jamais ignorée en silence ; une valeur du référentiel n'est jamais écrasée en silence.

| Colonne | Contenu |
|---|---|
| Champ | Le nom du champ, marqué « champ vide » si le référentiel n'a rien |
| Référentiel actuel | Valeur, source, commentaire |
| Fichier importé | Valeur, source, commentaire |
| On garde | Deux boutons radio, réf. ou fichier |

**Choix conseillé par défaut** : le fichier gagne quand le référentiel est vide, puisqu'il n'y a rien à perdre ; le référentiel gagne en cas de désaccord réel. Trois boutons permettent de tout basculer d'un côté, de l'autre, ou de revenir au conseil.

Ne sont pas listés : les champs identiques, et les **champs calculés**, qu'il serait absurde de reprendre puisqu'ils sont recalculés juste après. Le résumé en tête de fenêtre en donne le compte.

**Le sourçage suit sa valeur.** Prendre un chiffre du fichier reprend aussi son `_src` et son `_commentaire` : un nombre sans provenance n'a pas sa place dans le référentiel.

> **Le problème que cela résout.** Tenir une fiche enrichie à côté du référentiel était dangereux : à l'import, la version précédente ne proposait que les trous et laissait tomber le reste sans le dire. On perdait son travail sans s'en rendre compte. La fenêtre d'arbitrage rend toute divergence visible et tout écrasement délibéré.

### Blocs de réglages

Repliables, hors zone de capture, séparés par un trait. Facteurs d'échelle de police indépendants par zone (bandeau, commentaire, données, fiabilité, tableau, légende).

---

## 6. Outils, versions courantes et conformité

| Outil | Fichier | Rôle |
|---|---|---|
| Cartographie prospective et réseau | `cartographie-interactive-v18.html` | Carte du risque, fréquence par arrondissement, réseau, chronologie animée |
| Distance pélicandrome | `distance_pelicandrome_v11_1.html` | Rayon d'action depuis les stations au sol, fiches d'identité, tableau comparatif |
| Plans d'eau écopables | `plans-eau-ecopage.html` | Axes d'écopage mesurés, couverture de la flotte amphibie |
| Profil de vol d'écopage | `profil-vol-ecopage-v18.html` | Coupe latérale approche, écopage, décollage, moteur de légendes |
| Éditeur de flotte | `editeur-flotte.html` | Édition du référentiel commun, import CSV avec arbitrage champ par champ |
| Comparatif poids-puissance | `comparatif-ecopeurs-poids-puissance.html` | Rapport masse / puissance des écopeurs |
| Timeline des feux | `timeline feu/Timeline Incendie France.html` | Animation 2000-2026 par département |
| Dynamique sur 5 ans | `departement-incendie-5-ans-v2.html` | Surfaces brûlées rapportées au boisement |
| Feux européens, émissions | `europe-feux-emissions.html` | Surfaces UE et comparaison des émissions de CO2 |
| Feux européens, par pays | `europe-feux-par-pays.html` | Carte des 42 pays, part de forêt brûlée, dynamique 2025 |

Les versions antérieures présentes dans le dossier sont conservées à titre d'historique. **Ne pas les reprendre comme base.** Au 2026-08-18 : `profil-vol-ecopage-v17.html` est l'historique de la v18, et `flotte (1).json` est l'artefact de téléchargement qui porte en réalité la version la plus récente du référentiel (voir 6.1).

### 6.1 Inventaire réel au 2026-08-18

| Fichier annoncé | Situation |
|---|---|
| `plans-eau-france.json` | **Présent depuis le 2026-08-18.** Réextrait des données embarquées de `plans-eau-ecopage.html`. Extraction vérifiée fidèle : 1 731 axes identiques, 96 adjacences identiques, comptes 1 731 / 924 / 256 conformes. |
| `traite_region.py` | Toujours introuvable. Le script qui calcule les axes depuis un extrait Geofabrik n'est pas dans le dossier. La méthode est décrite en 7, l'outil non. |
| `rapport-reconstruction-feux-2051-2070.md` | Introuvable. |
| `timeline-incendie-france-v2.html` | Introuvable sous ce nom. Le dossier `timeline feu/` porte une version antérieure. |
| `chronologie-pelicandromes_4.json` | Remplacé par `chronologie-pelicandromes_4_1.json`. |
| `flotte (1).json` | **Supprimé le 2026-08-18.** Son contenu, le plus récent, est devenu `flotte.json`. Récupérable par `git checkout d4c7afb -- "flotte (1).json"`. |

**`gemini-code-1787015560089.py` n'est PAS `traite_region.py`.** Le fichier déposé dans le dossier applique une méthode entièrement différente, et beaucoup plus optimiste :

| | `gemini-code-*.py` | Méthode du projet |
|---|---|---|
| Mesure | Plus long côté du rectangle englobant orienté (`minimum_rotated_rectangle`) | Plus longue **corde inscrite**, par balayage rotatif |
| Largeur | Ignorée | Érosion de la moitié de la largeur requise |
| Polygones contigus | Non recollés | Recollés avant mesure |
| Source | Sandre / BD TOPAGE | Geofabrik / OSM |
| Sortie | `{id, nom, longueur_m, lat, lon}` | `{n, l, ha, d, a, b}` |

Le rectangle englobant surestime dès que le plan d'eau n'est pas rectiligne : un lac en croissant obtient une boîte longue alors qu'aucune course droite n'y tient. Son schéma de sortie est par ailleurs incompatible avec `axes[]`, faute des extrémités `a` et `b`. **À ne pas utiliser pour régénérer les axes.**

`export.geojson` (2,3 Mo, 22 juillet) est un extrait OSM brut : 1 512 polygones `natural=water`, sans nom ni département. C'est de la matière première, pas un résultat.

### Tableau de conformité au 2026-08-18, après la passe de synchronisation

| | Schéma v6 | Bloc embarqué | Dépendance distante | Captures conformes | Réglages exportables |
|---|---|---|---|---|---|
| `editeur-flotte.html` | complet | v6.2, 14 appareils | aucune | sans objet | brouillon localStorage |
| `distance_pelicandrome_v11_1.html` | complet | v6.2, 14 appareils | aucune | oui | oui |
| `profil-vol-ecopage-v18.html` | complet, via `PLANVOL` | v6.2, 14 appareils | aucune | à vérifier | oui |
| `plans-eau-ecopage.html` | complet | v6.2, 14 appareils | aucune | oui | **non** |
| `cartographie-interactive-v18.html` | sans objet | — | aucune | à vérifier | oui |
| `comparatif-ecopeurs-poids-puissance.html` | sans objet | — | aucune | à vérifier | non |
| `timeline feu/*.html` | sans objet | — | aucune | — | — |

Contrôles automatisés passés le 2026-08-18 :

- les quatre blocs embarqués sont **identiques** au tableau `fleet` de `flotte.json` ;
- les dix blocs de script des quatre outils passent `node --check` ;
- l'écart du modèle à trois phases est **nul sur les sept fiches écopeuses** ;
- aucune balise `<script src>` ni `<link href>` distante ne subsiste dans le dossier. Les seules requêtes sortantes restantes sont les **photos d'appareils**, distantes par conception, avec import depuis le disque et conversion en data-URI pour la capture.

### Articles

- `article-1-pelicandromes.md` — corrigé, augmenté du volet européen
- `article-2-avions-sol.md` — corrigé
- `rapport-reconstruction-feux-2051-2070.md` — méthode de reconstitution de la carte Chatry

---

## 7. Registre des faits vérifiés

À ne pas recalculer, à ne pas contredire sans nouvelle source.

### Réseau au sol

- 33 sites recensés. Nîmes-Garons est la seule station active toute l'année.
- Le retardant **Fire-Trol 931** est produit sur **un seul site français** : Biogema, aux Milles à Aix-en-Provence. Titulaire du marché DGSCGC pour la fourniture et la maintenance des stations.
- Environ 900 km d'Aix à Méaulte, le pélicandrome le plus éloigné, soit une douzaine d'heures de camion-citerne. Épinal est à environ 600 km.
- Dilution : **environ 20 %** de solution active (Perimeter Solutions, validé CEREN ; USDA donne 1 pour 4,75 sur le Fire-Trol 931). Le facteur de foisonnement est de **5 à 6, pas de 10**. Une erreur de ma part avait propagé le chiffre de 10 % dans l'article 1.
- Remplissage d'un Dash 8 : 6 à 10 minutes selon les sources. Pompes bridées à 1 800 L/min.
- Poteau d'incendie normalisé DN 100 : minimum **60 m³/h** sous 1 bar de pression résiduelle. Un rechargement en 6 à 8 minutes exige 75 à 100 m³/h. L'écart de 25 à 67 % justifie la cuve tampon.
- Bordeaux : 60 m³ de réserve, un avion à la fois. Cannes : 100 m³. Nîmes : 4 points retardant et 2 points eau.
- Goulot d'étranglement documenté par la DGSCGC : en 2022 Mérignac ne pouvait servir plus de 3 avions, rotation de 30 min pour un remplissage de 10 min. **Le facteur limitant est le nombre de postes, pas le débit d'eau.**
- Les DIR sont **deux unités militaires de la Sécurité civile** (statut militaire, employées et financées par l'Intérieur, non engagées par l'état-major des armées), positionnées à Brignoles, Nîmes et Lézignan-Corbières. Effectifs annoncés de 21 à 32 selon les sources. Unité de fabrication mobile : 18 000 L de retardant pur et deux cuves de 6 000 L d'eau. **Ligne de 10 m × 2 km en 90 minutes** (Wikipédia), pas 10.

### Flotte

- **12 Canadair CL-415**, 11 en état de voler depuis l'endommagement du Pélican 35 en 2025, 2 à 3 immobilisés en permanence. 95 exemplaires construits entre 1993 et 2015, dont 11 détruits. Acquisition française à environ 22 M€ l'unité, catalogue Bombardier autour de 30 M€. Aucune date de retrait officielle.
- CL-415, valeurs sourcées le 2026-08-01 : citerne certifiée **6 137 L** (1 621 US Gal), masse à vide **12,88 t** (Operating Weight Empty), masse au décollage **21,32 t** (*Maximum Lift Off Weight After Scooping*, 47 000 lbs) — la MTOW terrestre de 19,89 t ne s'applique pas à l'arrachement de l'eau.
- **8 Dash 8 Q400MR**, tous basés à Nîmes. 10 m³. Aucune capacité d'écopage.
- **CL-215** : 125 exemplaires construits, 15 en France dont 3 de remplacement, retirés en 1995-1996.
- **Tracker S-2FT** : retiré le **14 février 2020**. Ancien avion de lutte anti-sous-marine de l'US Navy converti par Conair. Sa piste courte explique la désaffectation d'Alès et du Luc.
- **Air Tractor AT-802F** : dérivé de l'AT-802 agricole. 3 000 à 3 100 L. **« Fire Boss » désigne la version amphibie à flotteurs**, absente de France. Aucun appareil détenu par la Sécurité civile, tous loués sous l'indicatif Abel.
- **DHC-515** : 4 commandés, 2 livrables en 2028, 2 en 2032-2033, près de 100 M€ l'unité. Flotte cible de 16 amphibies attendue à l'horizon 2033.
- **Kepplair 72** : conversion d'ATR 72, **7,5 t**, aucune commande ferme, 18 lettres d'intention non engageantes pour 300 à 400 M€. Certification EASA visée 2027.
- **A400M** : kit de 20 m³, essais Airbus depuis 2022, non certifié.
- **Salamandre S414** : **aucune source publique n'atteste son existence.** Concept transmis par l'utilisateur. Toutes ses valeurs sont non vérifiables. Citerne : 4 300 L d'eau, plus 400 L de concentré injecté pendant l'écopage.
- King Air B200 : 1 142 produits, 4 442 pour la famille Super King Air. Occasion 1,15 à 3,6 M$, King Air 260 neuf environ 6,7 M$. Motorisation 2 × 850 ch PT6A-42. **Piège d'identifiant : `BE200` désigne ici le Beechcraft King Air B200, pas le Beriev Be-200.** La confusion avait fait porter à la fiche la motorisation du Beriev (2 × 7 500 kgf, D-436TP), corrigée le 2026-07-26.

### Écopage

- CL-415 : 6 137 L en **410 à 450 m**, **9 à 12 secondes**, **130 à 160 km/h** selon les sources. Profondeur minimale 1,40 m. Hauteur de vol environ 2 m.
- Décomposition du contact retenue pour le CL-415 : environ 1,5 s d'amerrissage, 12 s de remplissage continu, 2,5 s d'arrachement, soit 16 s de contact total.
- Vitesse d'écopage retenue à 130 km/h (70 kts) : les 410 m en 12 s annoncés par le constructeur donneraient 66 kts, **sous la vitesse de décrochage** de 68 kts.
- Longueur de plan d'eau : les sources donnent 1 340 m annoncé comme minimum, 1 500 m couramment cité, **2 000 m × 100 m × 2 m de fond** décrit comme l'axe idéal par un chef de secteur Canadair de Nîmes.
- **Hauteurs de sécurité** : 50 ft (15,24 m) pour la distance d'atterrissage, **35 ft (10,67 m)** au décollage d'un avion à turbines (50 ft ne vaut que pour les avions à pistons). Ce sont des concepts de **certification sur piste** : aucun seuil réglementaire n'existe pour une course d'écopage. Les reprendre est une convention de lecture, à signaler comme telle.

### Feux, France

- 2022 : près de 66 000 ha, environ sept fois la moyenne des quinze années précédentes, la moitié en Gironde. Premiers incendies recensés en Loire-Atlantique et dans le Nord-Pas-de-Calais.
- 2025 : massif des Corbières, parmi les trois plus grands feux depuis la Seconde Guerre mondiale.
- Projections RCP 8.5 : part du territoire exposée de 27 à 64 % en zone Sud-Est, de 24 à 49 % en Sud-Ouest. Saison de 40 à 94 jours d'ici 2090 dans le Sud-Est, plus de 230 jours dans le Sud-Ouest.

### Feux, Europe

- Moyenne UE sur vingt ans : environ **354 000 ha/an**.
- 2017 : 988 524 ha. 2022 : près de 900 000. **2025 : 1 034 552 ha**, record, 7 783 incendies sur 25 pays.
- Périmètre élargi EFFIS (Europe, Moyen-Orient, Afrique du Nord) 2025 : 2 242 195 ha, dont **30 % pour la seule Ukraine** (environ 670 000 ha) et 39 % des départs. **Ces surfaces sont exclues du total européen pour raisons méthodologiques.**
- Émissions : **12,9 Mt de carbone** pour UE et Royaume-Uni en 2025, record, contre 11,4 Mt aux pics de 2003 et 2017. Converti en CO2 par le facteur 44/12 : environ **42 à 47 Mt CO2**.
- Comparaison : transports français 124,9 Mt CO2e en 2024, total national 367 Mt hors UTCATF.
- **Les feux de forêt sont comptabilisés dans l'UTCATF**, donc à l'intérieur du total national français, et non parmi les émissions naturelles (Citepa).
- Puits de carbone forestier français : environ 50 Mt CO2/an au milieu des années 2000, une quinzaine aujourd'hui. Les incendies ne sont qu'une des causes, avec la sécheresse, les maladies et la récolte.

### Plans d'eau écopables

- **1 731 axes** mesurés sur 22 régions, après retrait de 184 doublons inter-régions.
- Méthode : recollage des polygones contigus, érosion de la moitié de la largeur requise, recherche de la plus longue corde inscrite par balayage rotatif. Validée exacte sur formes de référence.
- Résultats à 60 m de largeur libre : 1 731 axes à 700 m, 924 à 1 000 m, 256 à 2 000 m.
- Facteur global entre le critère Canadair (2 000 m) et le critère court (700 m) : **environ 6,8**.
- **Limites à afficher systématiquement** : la profondeur n'est prise en compte nulle part, les obstacles non plus (ponts, câbles, lignes électriques), ni le marnage estival, ni le partage d'usage. Les chiffres sont une **borne haute de candidats**, pas une liste d'axes utilisables. Plusieurs résultats du Nord et de Normandie sont des bassins portuaires.

---

## 8. Pièges rencontrés, à ne pas reproduire

1. **CDN bloqués.** `d3js.org` et `jsdelivr` provoquent une page blanche. Toujours embarquer, sans exception de domaine.
2. **`crossorigin="anonymous"`** casse l'affichage des images distantes. Ne jamais l'utiliser.
3. **`ResizeObserver` non gardé** casse le script dans certains environnements.
4. **SVG sans `width`/`height`** donne une zone de 0 px si le script échoue.
5. **Codes ISO manquants.** France, Norvège, Malte et le Kosovo ont des codes numériques absents ou nuls dans Natural Earth. Prévoir une table de rattrapage manuelle.
6. **Union globale de polygones** sature la mémoire au-delà d'environ 40 000 éléments. Passer par une adjacence spatiale et une structure union-find, puis n'unir qu'à l'intérieur des composantes.
7. **Rivières fragmentées.** Les couches hydrographiques livrent les cours d'eau en tronçons. Sans recollage préalable, on mesure des segments de 400 m au lieu d'un chenal de 5 km.
8. **Opacité pour marquer un état.** Une opacité de 55 % sur un aplat rouge donne un marron parasite. Préférer un anneau pointillé.
9. **Ordre d'initialisation.** Une fonction de rendu appelée avant le calcul de la géométrie lève une exception silencieuse attrapée par le `try/catch`, ce qui laisse la page à moitié construite.
10. **Un ratio nul n'est pas une absence de donnée.** Un pays sans aucun feu doit se colorer à l'extrémité verte, pas en gris.
11. **Deviner une valeur numérique depuis un champ texte.** `plans-eau-ecopage.html` reconstruit `tankL` en dépouillant `tank` de ses caractères non chiffrés : « 4 300 L d'eau + 400 L de concentré » devient **4 300 400 L**. Et il devine `minWater` en cherchant un motif dans la phrase `scoop`, si bien qu'importer le `flotte.json` actuel met **tous** les appareils à `minWater = 0` et vide la carte. Ne jamais déduire un nombre d'une phrase : lire le champ numérique, ou laisser vide.
12. **Concaténer deux nombres au lieu de choisir.** `citerne_l` du S414 valait **43004**, soit « 4 300 » et « 400 » collés. Une citerne à un ordre de grandeur au-dessus du reste de la flotte n'a produit aucune alerte. Prévoir un contrôle de vraisemblance sur les grandeurs bornées.
13. **Un bloc embarqué périmé ne se voit pas.** Un outil dont les données embarquées ont un mois de retard s'ouvre normalement et affiche des chiffres faux. Vérifier `meta.derniere_maj` du bloc embarqué contre le fichier de référence à chaque intervention.
14. **Un export partiel écrase un référentiel complet.** Trois outils exportaient sous des noms différents et réécrivaient `meta`. Un export depuis `plans-eau` remplaçait 12 appareils et 113 champs par 10 appareils et 33 champs, sous le nom `flotte.json`. Voir la règle 3.3.
15. **Confondre une phase et un total.** Les 410 à 450 m publiés pour le CL-415 décrivent la phase efficace ; `ecopage_duree_s` décrit le contact total. Mettre l'un en face de l'autre produisait un écart de 38 %, que l'outil signalait sans que personne le lise. Toujours vérifier de quelle phase parle un chiffre de constructeur avant de le poser dans un champ. Voir 3.5 bis.
16. **Chercher une fonction par son nom supposé.** `syncDepuisFlotte()` existait déjà dans `profil-vol` et tournait au démarrage, mais une recherche sur les noms de champs `ecopage_*` limitée au début du fichier n'avait ramené que le bloc de données embarqué. Conclusion tirée : « aucun outil ne lit le référentiel de plan de vol », et un second dispositif a failli être écrit à côté du premier. Sur ces fichiers monolithiques, chercher un **comportement** par plusieurs motifs et sur toute la longueur, jamais par un seul nom.
18. **Un chiffre calculable saisi à la main.** Le contact total d'écopage avait été posé en dur dans le JSON. Il fallait le recalculer à chaque modification d'une durée, ce que personne ne fait. Toute grandeur dérivable appartient au bloc de calcul partagé et se marque `_src: calcul`.
19. **Le cache du serveur local masque une correction.** Après réécriture d'un fichier, `python -m http.server` peut renvoyer une copie en cache et le navigateur affiche l'ancien état. Un contrôle de rendu doit forcer le rechargement (`?v=` + horodatage) avant de conclure quoi que ce soit.
20. **Une police n'est pas un script, mais elle se charge quand même à distance.** `comparatif-ecopeurs` appelait `fonts.googleapis.com`. L'échec ne donne pas de page blanche, il décale une mise en page calibrée au pixel : la capture ne ressemble plus à l'écran. Embarquer aussi les polices. Attention aux **polices variables** : Google sert le même fichier pour toutes les graisses demandées, l'embarquer une fois par graisse triple le poids pour rien.

---

## 9. Décisions d'architecture arrêtées

Toutes datées du 2026-08-18, prises à l'issue de l'audit. Elles priment sur le code existant.

| # | Décision | État |
|---|---|---|
| 1 | Le commentaire canonique est `<champ>_commentaire`, construit sur le nom complet du champ. Les quatre formes tronquées historiques migrent puis disparaissent. | appliquée |
| 2 | Une ligne de flotte **par variante**, pas par famille. `id` est la seule clé de liaison entre outils. | appliquée |
| 3 | **Aucun CDN**, aucune exception de domaine. D3, html2canvas et les polices s'embarquent. | appliquée |
| 4 | Tout outil peut exporter la flotte, sous le nom `flotte.json`, en **conservant le `meta` reçu** et en n'ajoutant qu'une ligne d'horodatage. Les champs inconnus de l'outil sont recopiés tels quels. | appliquée sur `plans-eau` |
| 5 | `citerne_l` du S414 passe de 43004 à **4300** (eau seule). Le concentré reste décrit dans le commentaire. | appliquée |
| 6 | Pour le plan de vol, **la flotte fait foi**, le fichier de profils ne porte que l'affichage. | appliquée |
| 7 | Ajout de `qty_n` numérique. `qty` reste le texte affiché et **ne doit jamais être parsé**. | appliquée |
| 8 | `ecopage_distance_m` est la course sur l'eau **TOTALE**, somme des trois phases. Les 410 à 450 m publiés pour un Canadair décrivent la seule phase efficace. Voir 3.5 bis. | appliquée |
| 9 | Pour un écopeur, `loadedMass` affiche la masse à l'**arrachement de l'eau**, pas la MTOW terrestre. Le CL-415 passe de 19,9 à 21,32 t. | appliquée |
| 10 | Modèle **saisie / calcul**. Par phase d'écopage on saisit la durée **ou** la distance ; l'autre, les totaux et `longueur_min_m` sont dérivés par le bloc de calcul partagé, jamais posés à la main. Nouveau statut `_src` : `calcul`. | appliquée |
| 11 | `longueur_min_m` devient une **grandeur formelle** : moyenne du cycle le plus court et du cycle le plus long, d'un seuil de 50 m à l'autre. Les longueurs publiées, trop dispersées, ne servent plus de référence. | appliquée |
| 12 | Les calculs d'écopage vivent dans **un seul bloc de code, dupliqué à l'identique** dans les quatre outils par un script d'injection. Aucune formule recopiée ailleurs. | appliquée |
| 13 | Le moteur a ses propres champs : `moteur_nombre` et `moteur_reference` saisis, `enginePower` et la puissance unitaire calculés. | appliquée |
| 14 | L'import d'une fiche isolée passe par un **arbitrage complet** ancien / nouveau, sourçage affiché des deux côtés. Aucune valeur reprise ni ignorée sans choix explicite. | appliquée |

`qty_n` vaut le nombre d'appareils réellement en service en France : 12 pour le CL-415, 8 pour le Dash 8, 3 pour le King Air, **0 partout ailleurs** — y compris pour les appareils loués en quantité variable et pour les commandes non livrées, dont la nuance reste dans `qty` et `qtyNote`.

---

## 10. Chantier en cours

Objectif principal : porter `plans-eau-ecopage.html` au niveau des autres outils. Il est resté en v1 et cumule les écarts.

### Fait le 2026-08-18

0. ~~Sauver la donnée.~~ `plans-eau-france.json` réextrait et vérifié fidèle. `flotte (1).json` fusionné dans `flotte.json` puis supprimé.
1. ~~Corriger le référentiel.~~ `citerne_l` du S414 à 4 300, `qty_n` créé sur les 14 fiches, les quatre commentaires tronqués migrés (47 valeurs déplacées), variantes `AT802FB` et `FF72S` créées, ordre des clés normalisé, `meta.version` porté à `2026-08-18-v6.2`.
2. ~~Resynchroniser les blocs embarqués.~~ Les quatre outils portent le même tableau `fleet`, contrôle automatisé à l'appui.
3. ~~Refondre la fiche d'identité de `plans-eau`.~~ Schéma v6, commentaires en gris tirés du JSON, libellés fixes, cinq statuts, lignes conditionnelles sur `modification_avion_existant`, photo en `<img referrerpolicy>`.
4. ~~Réparer l'import de flotte de `plans-eau`.~~ Plus aucune devinette sur `scoop` ni `tank`. L'adaptateur legacy ne se déclenche que si `mode_recharge` est absent, et le signale à l'écran.
5. ~~Réparer l'export de `plans-eau`.~~ Il conserve le `meta` reçu et n'ajoute qu'une ligne d'horodatage.
6. ~~Modale d'édition de `plans-eau`~~ : ne se ferme plus au clic extérieur.
7. ~~Captures de `plans-eau`~~ : marge de 10 px posée puis retirée, nom préfixé par le sujet, conversion des images en data-URI et avertissement annulable.
8. ~~Lecteurs des anciens noms de commentaire~~ : `distance_pelicandrome` lit et écrit désormais la forme canonique. Sa table `CORRESP` dans `profil-vol` pointe sur les nouvelles variantes.

### Fait le 2026-08-18, deuxième passe

9. ~~Embarquer les dépendances.~~ 9 balises `<script src>` remplacées, dont deux vers `d3js.org`. Polices Google du comparatif en data-URI, dédoublonnées par détection des polices variables.
10. ~~Plan de vol des écopeurs.~~ Modèle à trois phases renseigné sur les sept fiches, `ecopage_distance_m` redéfini comme la course totale, écart tombé à zéro partout. Deux impossibilités corrigées au passage : durée efficace supérieure à la durée totale sur le DHC-515 et le CL-215, 35 s de contact sur le Fire Boss.
11. ~~La flotte fait foi pour le plan de vol.~~ La reprise couvre désormais toute la bibliothèque et pas seulement le profil actif, un bandeau signale les écarts, un bouton force la reprise, et l'import d'un référentiel la déclenche.
12. ~~Champs texte hérités.~~ `emptyMass` et `loadedMass` réalignés sur les valeurs numériques sourcées.

### Effet de la longueur de plan d'eau formelle

Le passage d'une longueur saisie à une longueur calculée au seuil de 50 m change beaucoup de choses, et il faut le savoir avant de citer un chiffre.

| Appareil | Longueur saisie, avant | Longueur calculée | Axes accessibles avant | Après | Variation |
|---|---|---|---|---|---|
| Canadair CL-415 | 1 500 m | **1 773 m** | 426 | 316 | −26 % |
| Canadair CL-215 | 1 500 m | **1 921 m** | 426 | 278 | −35 % |
| DHC-515 | 1 500 m | **1 957 m** | 426 | 267 | −37 % |
| AT-802F Fire Boss | 1 000 m | **1 657 m** | 924 | 358 | −61 % |
| Hynaero Frégate-F100 | 800 m | **1 945 m** | 1 372 | 269 | −80 % |
| Positive Aviation FF72-S | non publiée | **2 185 m** | — | 221 | — |
| Salamandre S414 | 700 m | **1 524 m** | 1 731 | 419 | −76 % |

Sur 1 731 axes mesurés.

**Ce que ce changement fait au raisonnement.** Les longueurs saisies décrivaient la course sur l'eau ; la longueur calculée décrit la **manœuvre complète, obstacle de 50 m compris aux deux bouts**. Ce ne sont pas les mêmes grandeurs, et le classement des appareils s'en trouve modifié :

- l'écart entre appareils se resserre fortement. Le F100 perd l'avantage de son écopage court (490 m efficaces contre 433 au CL-415) parce que sa montée nominale à 4° coûte 715 m contre 572 au Canadair ;
- le F100 et le DHC-515 finissent à deux mètres l'un de l'autre, 1 945 contre 1 957, alors qu'ils étaient annoncés à 800 et 1 500 m ;
- seul le S414, avec 345 m de course sur l'eau, garde un avantage net.

Autrement dit, **sous cette convention, un appareil se distingue par ses angles bien plus que par ses écopes**. C'est cohérent : à 3°, la descente depuis 50 m occupe déjà 954 m, soit plus que n'importe quelle course sur l'eau de la flotte.

Deux paramètres méritent d'être discutés avant de publier quoi que ce soit à partir de ces chiffres : le seuil de 50 m, et le fait que les angles nominaux et maximaux de la plupart des appareils sont des ordres de grandeur non sourcés.

### Fait le 2026-08-18, troisième passe

13. ~~Modèle saisie / calcul.~~ Six champs nouveaux (`ecopage_distance_avant_m`, `_efficace_m`, `_apres_m`, `ecopage_duree_apres_s`), règle de trois dans les deux sens, champs dérivés grisés dans l'éditeur.
14. ~~Bloc de calcul partagé.~~ 165 lignes, injectées à l'identique dans les quatre outils, appelées au chargement, à l'import et à la validation d'une fiche.
15. ~~`longueur_min_m` formelle.~~ Calculée au seuil de 50 m sur les sept fiches écopeuses.
16. ~~Import d'une fiche isolée dans l'éditeur.~~ Ne remplit que les trous, crée l'appareil s'il est absent.
17. ~~Commentaires de dette.~~ 46 formules décrivant l'historique de migration remplacées par ce qui est su de la provenance. Aucune valeur ni aucun `_src` touché.

### Fait le 2026-08-18, quatrième passe

18. ~~Champs moteur.~~ `enginePower` éclaté en `moteur_nombre` + `moteur_reference` + `puissance_ch`, le texte d'affichage devenant calculé. Ligne « Motorisation » ajoutée aux fiches de `plans-eau` et de `distance_pelicandrome`.
19. ~~Arbitrage à l'import d'une fiche.~~ Fenêtre complète ancien / nouveau avec sourçage des deux côtés, choix par ligne, bascule globale, champs calculés exclus.
20. ~~Audit du calcul de `longueur_min_m`.~~ Vérifié égal à la médiane du cycle à 50 m sur les sept fiches écopeuses, et identique dans `flotte.json` et les quatre blocs embarqués. La valeur est portée au bandeau du profil de vol, en turquoise à côté du nom.

### Reste à faire

1. **Propager la passe de sourçage aux grandeurs hors plan de vol.** Masses, puissances, prix et cadences portent encore des commentaires de dette (« Source à retrouver ») sur la plupart des fiches. Le plan de vol est fait, le reste non.
2. **Export des réglages de `plans-eau`** sous une clé `plansEau` dans `parametres-utilisateur-pelicandromes.json`, selon la convention de 4.4. C'est le dernier écart de `plans-eau` au cahier des charges.
3. **Dimensions de plan d'eau du FF72-S** : non publiées, la fiche ne peut donc pas être placée sur la carte des plans d'eau. À sourcer ou à estimer explicitement.
4. **Valeurs du Fire Boss** : la fiche `AT802FB` hérite des masses et de la citerne de la cellule terrestre, sans correction de la pénalité de masse et de traînée des flotteurs. Seule la durée de remplissage est sourcée.
5. **Citerne du FF72 et du FF72-S** : `citerne_l` vaut 0, « non publié avec certitude ». Un bombardier d'eau à 0 L fausse tout tableau comparatif.
6. **Profil Beriev Be-200 Altair** : non relié à la flotte, il garde ses valeurs d'origine, dont une durée efficace supérieure à la durée totale. Soit on lui crée une fiche, soit on retire le profil.
7. **Supprimer `CORRESP`** en alignant les noms de profil sur les noms de flotte, pour que la liaison se fasse directement par `id`.

---

## 11. Points ouverts

- Le pélicandrome mobile de **Melun-Villaroche**, les **trois Dash déployés** à Fontainebleau et le **largage toutes les quinze minutes** ne sont attestés par aucune source que j'aie pu consulter.
- Les essais A400M au retardant « il y a quelques semaines », le délai d'installation de deux heures et le nombre d'Air Tractor loués (six à huit) restent à sourcer.
- La question de savoir si les stations **fixes** stockent du concentré ou du produit prêt à l'emploi n'est pas tranchée. Les descriptions de SDIS disent prêt à l'emploi, mais toutes les installations examinées comportent deux cuves distinctes, ce qui plaide pour un mélange sur place. L'ambiguïté est signalée dans l'article 1.
- La table `dbData` de l'outil « dynamique sur 5 ans » (taux de boisement et surfaces brûlées par département) est héritée et non sourcée.
- Le graphique en barres de tous les feux, évoqué par l'utilisateur, reste introuvable dans les conversations accessibles. Il a peut-être été créé dans un Projet Claude, invisible depuis une conversation ordinaire.
- Treize fiches sur quatorze portent encore des commentaires de sourçage automatiques (« Repris du profil de vol v19 », « Source à retrouver »). Ce sont des marqueurs de dette, pas des sources.
- Le script qui a produit les 1 731 axes reste introuvable. Sans lui, les axes ne peuvent pas être recalculés : `plans-eau-france.json` est aujourd'hui la seule trace du résultat.

---

## 12. Suite éditoriale prévue

Article 3 : les avions opérant depuis les plans d'eau. Cartographie du maillage des plans d'eau adaptés à chaque catégorie d'appareil, capacités du Canadair et de ses successeurs possibles, opérabilité depuis un pélicandrome puis depuis un plan d'eau. Puis, en article 3 ou 4, l'hypothèse du drone écopeur lourd, à traiter de façon comparative et honnête.
