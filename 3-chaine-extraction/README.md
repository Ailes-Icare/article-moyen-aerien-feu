# La chaîne d'extraction

Cinq scripts Python qui produisent `2-donnees/ecopage/plans-eau-france.json` à
partir des données OpenStreetMap.

**Vous n'en avez besoin que pour régénérer les données géographiques.** Pour
utiliser les outils, le fichier est déjà là et ce dossier ne vous concerne pas.

Mode d'emploi complet :
**[la fiche de la chaîne d'extraction](../5-documentation/11-chaine-extraction.md)**

---

## En résumé

```bash
python -m pip install geopandas shapely pyproj   # une seule fois, ~150 Mo

python telecharge_geofabrik.py                    # ~8 Go, 6 min
python extrait_toutes.py                          # 10 min
python consolide_axes.py                          # quelques secondes
```

| Script | Rôle |
|---|---|
| `telecharge_geofabrik.py` | Récupère les 22 extraits régionaux OpenStreetMap et en extrait les couches d'eau |
| `traite_region.py` | Mesure les courses d'écopage d'une région — le cœur géométrique |
| `extrait_toutes.py` | Enchaîne le précédent sur les 22 régions, quatre de front |
| `consolide_axes.py` | Dédoublonne, affecte les départements, nettoie, assemble la France |
| `test_courses.py` | Banc de test — **à lancer après toute modification de la géométrie** |

---

## Deux avertissements

**La couche `_a_`.** `gis_osm_water_a_free_1` est la couche des **surfaces**,
`gis_osm_waterways_free_1` celle des **lignes**. Un seul caractère les sépare.
Se tromper ne provoque aucune erreur : le script calcule des aires, une ligne a
une aire nulle, et le résultat est zéro axe. Un échec parfaitement silencieux.

**Le banc de test.** `test_courses.py` vérifie huit propriétés sur des formes
dont la réponse est connue. Il tourne en quelques secondes et attrape les
régressions que rien d'autre ne verrait.
