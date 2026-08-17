# Projet « Moyens aériens de lutte contre les feux de forêt »

Document de reprise. Il décrit le cahier des charges permanent des infographies, l'état de chaque outil, la structure des données, les faits vérifiés, et les pièges déjà rencontrés.

À lire en entier avant toute modification d'un outil.

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

- **D3 doit être embarqué dans le fichier**, jamais chargé depuis un CDN. Environ 280 Ko.
  Motif : `d3js.org` et `cdn.jsdelivr.net` sont bloqués dans certains environnements, ce qui a produit deux pages entièrement blanches sans le moindre message d'erreur.
- Les **fonds de carte GeoJSON sont embarqués**, jamais chargés à distance.
- Tout script doit être **enveloppé dans un `try/catch`** qui affiche l'erreur en rouge en haut de page. Une page blanche silencieuse est le pire des échecs.
- Les `<svg>` portent des attributs `width` et `height` **explicites**, en plus du `viewBox`. Sans quoi ils font 0×0 si le script échoue.
- `ResizeObserver` doit être gardé : `if (typeof ResizeObserver !== "undefined")`. Sinon le script casse dans certains environnements.

### Captures d'écran

- Marge de **10 px sur les quatre côtés**, ajoutée avant la capture et retirée après.
- Nom de fichier **préfixé par le sujet** (appareil sélectionné, région, etc.).
- Vérification **avant** production du fichier, avec possibilité d'annuler.
- Sur les images distantes : ne **jamais** poser `crossorigin="anonymous"` sur une balise `<img>`. Cet attribut force une requête CORS et fait échouer l'affichage chez la majorité des hébergeurs. Utiliser `referrerpolicy="no-referrer"` seul.
- Conséquence : une image affichée sans CORS ne peut pas être peinte par html2canvas. Deux parades, à proposer à l'utilisateur : importer le fichier depuis le disque (converti en data-URI, toujours capturable), ou l'héberger sur `raw.githubusercontent.com`, qui envoie `Access-Control-Allow-Origin: *`.

### Données

- Les JSON de référence sont **embarqués en dur** dans chaque outil, dans un bloc encadré par des bandeaux de commentaire `BLOC DE DONNÉES EMBARQUÉES — DÉBUT / FIN`, avec la correspondance fichier ↔ constante indiquée.
- Les boutons d'import restent disponibles et écrasent ces valeurs à chaud.
- Tout réglage utilisateur doit être **exportable et réimportable en JSON**.
- Exception documentée : l'état coché/décoché des familles de sites n'est ni sauvegardé ni rechargé, à la demande de l'utilisateur, pour que les défauts se réappliquent à chaque ouverture.

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

## 3. Outils, versions courantes

| Outil | Fichier | Rôle |
|---|---|---|
| Cartographie prospective et réseau | `cartographie-interactive-v18.html` | Carte du risque, carte fréquence par arrondissement, réseau des pélicandromes, chronologie animée |
| Distance pélicandrome | `distance_pelicandrome_v11.html` | Rayon d'action de la flotte depuis les stations au sol, fiches d'identité, tableau comparatif |
| Plans d'eau écopables | `plans-eau-ecopage.html` | Axes d'écopage mesurés, couverture de la flotte amphibie |
| Timeline des feux | `timeline-incendie-france-v2.html` | Animation 2000-2026 des incendies par département |
| Dynamique sur 5 ans | `departement-incendie-5-ans-v2.html` | Surfaces brûlées rapportées au boisement |
| Feux européens, émissions | `europe-feux-emissions.html` | Surfaces UE et comparaison des émissions de CO2 |
| Feux européens, par pays | `europe-feux-par-pays.html` | Carte des 42 pays, part de forêt brûlée, dynamique 2025 |
| Profil de vol d'écopage | `profil-vol-ecopage.html` | Coupe latérale approche, écopage, décollage, avec moteur de légendes |
| Script de traitement | `traite_region.py` | Calcul des axes d'écopage depuis un extrait Geofabrik |

Les versions antérieures présentes dans le dossier sont conservées à titre d'historique. **Ne pas les reprendre comme base.**

### Articles

- `article-1-pelicandromes.md` — corrigé, augmenté du volet européen
- `article-2-avions-sol.md` — corrigé
- `rapport-reconstruction-feux-2051-2070.md` — méthode de reconstitution de la carte Chatry

---

## 4. Fichiers de données

| Fichier | Contenu | Clé |
|---|---|---|
| `chronologie-pelicandromes_4.json` | 33 sites : position, type, date de création, changements de statut, sources | `sites.<id>` |
| `flotte-pelicandromes_5.json` | 12 appareils, dont 6 écopeurs | `fleet[]` |
| `carte2-data-v2.json` | Couleurs de la carte fréquence, logique poupée russe | clé 2 car. = département, 5 car. = arrondissement |
| `plans-eau-france.json` | 1 731 axes d'écopage dédoublonnés, 96 départements, adjacences | `axes[]` |
| `axes-ecopage-<région>.geojson` | 22 fichiers régionaux, 1 915 axes bruts avant dédoublonnage | |

### Séparation des responsabilités, à respecter

- `flotte-*.json` ne contient **que** les aéronefs. Aucune position, aucun statut de station.
- `chronologie-*.json` porte **l'intégralité** du réseau : position, statut courant, historique daté.
- Ajouter un pélicandrome se fait dans la chronologie **seule**.
- Historique : jusqu'en v3, la flotte portait aussi le réseau, parce que seul l'outil Distance Pélicandrome avait une fonction d'ajout manuel d'aérodrome et que son export sérialisait tout. Corrigé en v4.

### Conventions du JSON de flotte

- `mode_recharge` : booléen. `true` = écopage sur plan d'eau **et** pélicandrome ; `false` = pélicandrome exclusivement. Libellé fixe côté outil.
- `modification_avion_existant` : `true` = kit de conversion sur cellule existante.
- `base_cellule_occasion` : `true` = cellule de départ d'occasion.
- Les champs `prix_kit` et `cadence_production_kit` ne s'affichent que pour une conversion.
- Principe général : chaque grandeur exploitée par un algorithme existe en **valeur brute chiffrée** plus un **attribut commentaire** en texte libre.

---

## 5. Registre des faits vérifiés

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
- **8 Dash 8 Q400MR**, tous basés à Nîmes. 10 m³. Aucune capacité d'écopage.
- **CL-215** : 125 exemplaires construits, 15 en France dont 3 de remplacement, retirés en 1995-1996.
- **Tracker S-2FT** : retiré le **14 février 2020**. Ancien avion de lutte anti-sous-marine de l'US Navy converti par Conair. Sa piste courte explique la désaffectation d'Alès et du Luc.
- **Air Tractor AT-802F** : dérivé de l'AT-802 agricole. 3 000 à 3 100 L. **« Fire Boss » désigne la version amphibie à flotteurs**, absente de France. Aucun appareil détenu par la Sécurité civile, tous loués sous l'indicatif Abel.
- **DHC-515** : 4 commandés, 2 livrables en 2028, 2 en 2032-2033, près de 100 M€ l'unité.
- **Kepplair 72** : conversion d'ATR 72, **7,5 t**, aucune commande ferme, 18 lettres d'intention non engageantes pour 300 à 400 M€. Certification EASA visée 2027.
- **A400M** : kit de 20 m³, essais Airbus depuis 2022, non certifié.
- **Salamandre S414** : **aucune source publique n'atteste son existence.** Concept transmis par l'utilisateur. Toutes ses valeurs sont non vérifiables.
- King Air B200 : 1 142 produits, 4 442 pour la famille Super King Air. Occasion 1,15 à 3,6 M$, King Air 260 neuf environ 6,7 M$.

### Écopage

- CL-415 : 6 137 L en **410 à 450 m**, **9 à 12 secondes**, **130 à 160 km/h** selon les sources. Profondeur minimale 1,40 m. Hauteur de vol environ 2 m.
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

## 6. Pièges rencontrés, à ne pas reproduire

1. **CDN bloqués.** `d3js.org` et `jsdelivr` provoquent une page blanche. Toujours embarquer.
2. **`crossorigin="anonymous"`** casse l'affichage des images distantes. Ne jamais l'utiliser.
3. **`ResizeObserver` non gardé** casse le script dans certains environnements.
4. **SVG sans `width`/`height`** donne une zone de 0 px si le script échoue.
5. **Codes ISO manquants.** France, Norvège, Malte et le Kosovo ont des codes numériques absents ou nuls dans Natural Earth. Prévoir une table de rattrapage manuelle.
6. **Union globale de polygones** sature la mémoire au-delà d'environ 40 000 éléments. Passer par une adjacence spatiale et une structure union-find, puis n'unir qu'à l'intérieur des composantes.
7. **Rivières fragmentées.** Les couches hydrographiques livrent les cours d'eau en tronçons. Sans recollage préalable, on mesure des segments de 400 m au lieu d'un chenal de 5 km.
8. **Opacité pour marquer un état.** Une opacité de 55 % sur un aplat rouge donne un marron parasite. Préférer un anneau pointillé.
9. **Ordre d'initialisation.** Une fonction de rendu appelée avant le calcul de la géométrie lève une exception silencieuse attrapée par le `try/catch`, ce qui laisse la page à moitié construite.
10. **Un ratio nul n'est pas une absence de donnée.** Un pays sans aucun feu doit se colorer à l'extrémité verte, pas en gris.

---

## 7. Points ouverts

- Le pélicandrome mobile de **Melun-Villaroche**, les **trois Dash déployés** à Fontainebleau et le **largage toutes les quinze minutes** ne sont attestés par aucune source que j'aie pu consulter.
- Les essais A400M au retardant « il y a quelques semaines », le délai d'installation de deux heures et le nombre d'Air Tractor loués (six à huit) restent à sourcer.
- La question de savoir si les stations **fixes** stockent du concentré ou du produit prêt à l'emploi n'est pas tranchée. Les descriptions de SDIS disent prêt à l'emploi, mais toutes les installations examinées comportent deux cuves distinctes, ce qui plaide pour un mélange sur place. L'ambiguïté est signalée dans l'article 1.
- La table `dbData` de l'outil « dynamique sur 5 ans » (taux de boisement et surfaces brûlées par département) est héritée et non sourcée.
- Le graphique en barres de tous les feux, évoqué par l'utilisateur, reste introuvable dans les conversations accessibles. Il a peut-être été créé dans un Projet Claude, invisible depuis une conversation ordinaire.

---

## 8. Suite prévue

Article 3 : les avions opérant depuis les plans d'eau. Cartographie du maillage des plans d'eau adaptés à chaque catégorie d'appareil, capacités du Canadair et de ses successeurs possibles, opérabilité depuis un pélicandrome puis depuis un plan d'eau. Puis, en article 3 ou 4, l'hypothèse du drone écopeur lourd, à traiter de façon comparative et honnête.
