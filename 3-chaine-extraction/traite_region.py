#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Axes d'ecopage a partir d'un extrait Geofabrik (couche gis_osm_water_a_free_1).

    python3 traite_region.py <chemin.shp> <NomRegion> [seuils]

Sortie : GeoJSON des axes + une ligne de synthese par seuil (volontairement compact).
Concu pour survivre a un reset de conteneur : aucun etat externe, tout est recalcule.
"""
import sys, os, time, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import geopandas as gpd
from collections import defaultdict, Counter
from shapely.strtree import STRtree
from shapely.ops import unary_union
from shapely.geometry import MultiPolygon, Polygon, LineString
from shapely import affinity
from pyproj import Transformer

SHP    = sys.argv[1]
REGION = sys.argv[2] if len(sys.argv) > 2 else "region"
SEUILS = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [700, 1000, 1340, 1500, 2000, 3000]
W      = 60          # largeur libre imposee (m) - l'effet largeur est marginal, cf. analyse
# Ecartement minimal entre les milieux de deux courses retenues sur un meme
# plan d'eau. Meme logique que le pas d'echantillonnage du trait de cote :
# une etendue longue couvre une distance, elle vaut donc un point tous les
# tant de metres et non un point unique en son milieu. Surchargeable par
# variable d'environnement pour pouvoir regler la granularite sans editer.
ECART_MIN_M = int(os.environ.get("AXES_ECART_M") or 5000)
OUTDIR = os.environ.get("AXES_OUTDIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "sorties-axes")
os.makedirs(OUTDIR, exist_ok=True)

t_start = time.time()

# ---------- 1. chargement, filtrage, projection ----------
g = gpd.read_file(SHP)
n_brut = len(g)
EXCLURE = {c for c in g["fclass"].unique() if str(c).startswith("wetland")} | {"dock"}
g = g[~g["fclass"].isin(EXCLURE)]
g = g.to_crs("EPSG:2154")                      # Lambert-93, metres
g["geometry"] = g.geometry.buffer(0)           # reparation topologique
g = g[~g.geometry.is_empty & g.geometry.notna()].copy()
g["area"] = g.geometry.area
g = g[g["area"] > 1000].reset_index(drop=True)  # bruit : mares < 0,1 ha
t_load = time.time() - t_start

# ---------- 2. recollage par composantes connexes ----------
# L'union globale sature la memoire au-dela de ~40k polygones : on passe par
# une adjacence spatiale + union-find, puis on n'unit qu'a l'interieur des
# composantes multi-membres. Indispensable pour les rivieres, livrees en troncons.
t0 = time.time()
geoms = np.array(g.geometry.values, dtype=object)
n = len(geoms)
pairs = STRtree(geoms).query(geoms, predicate="dwithin", distance=2.0)

parent = np.arange(n)
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for a, b in zip(pairs[0], pairs[1]):
    if a != b:
        ra, rb = find(int(a)), find(int(b))
        if ra != rb: parent[rb] = ra

comp = defaultdict(list)
for i in range(n): comp[find(i)].append(i)

areas_in = g["area"].values
name_arr = g["name"].values
AIRE_MIN = min(SEUILS) * W * 0.95
parts, names = [], []
for idx in comp.values():
    if areas_in[idx].sum() < AIRE_MIN:
        continue
    merged = geoms[idx[0]] if len(idx) == 1 else \
             unary_union([geoms[i].buffer(1.0) for i in idx]).buffer(-1.0)
    subs = merged.geoms if isinstance(merged, MultiPolygon) else [merged]
    cand = [(areas_in[i], name_arr[i]) for i in idx if isinstance(name_arr[i], str)]
    nm = max(cand)[1] if cand else None
    for p in subs:
        if isinstance(p, Polygon) and p.area >= AIRE_MIN:
            parts.append(p); names.append(nm)
t_merge = time.time() - t0

# ---------- 3. plus long couloir rectiligne inscrit ----------
# Erosion de W/2 (la marge laterale devient implicite), puis balayage rotatif
# a la recherche de la plus longue corde. Valide exact sur formes de reference.
parts_s = [p.simplify(5.0, preserve_topology=True).buffer(0) for p in parts]

def longest_run(poly, width_m, angle_step=3.0, max_scan=48):
    eroded = poly.buffer(-width_m / 2.0)
    if eroded.is_empty: return 0.0, None
    subs = list(eroded.geoms) if isinstance(eroded, MultiPolygon) else [eroded]
    best_len, best_line = 0.0, None
    for part in subs:
        if part.is_empty or part.area <= 0: continue
        minx, miny, maxx, maxy = part.bounds
        cx, cy = part.centroid.x, part.centroid.y
        for ang in np.arange(0, 180, angle_step):
            rot = affinity.rotate(part, -ang, origin=(cx, cy))
            rminx, rminy, rmaxx, rmaxy = rot.bounds
            step = max(width_m / 2.0, (rmaxy - rminy) / max_scan)
            y = rminy + step / 2.0
            while y <= rmaxy:
                inter = rot.intersection(LineString([(rminx - 10, y), (rmaxx + 10, y)]))
                if not inter.is_empty:
                    segs = [inter] if inter.geom_type == "LineString" else \
                           [s for s in getattr(inter, "geoms", []) if s.geom_type == "LineString"]
                    for s in segs:
                        if s.length > best_len:
                            best_len = s.length
                            best_line = affinity.rotate(s, ang, origin=(cx, cy))
                y += step
    return best_len, best_line


def toutes_courses(poly, width_m, Lmin, angle_step=3.0, max_scan=48):
    """Toutes les courses DISTINCTES inscrites dans poly, la plus longue en tete.

    longest_run enumere deja tous les segments admissibles, a tous les angles
    et toutes les lignes de balayage, puis n'en retient qu'un seul. Une Loire
    de 30 km en ressortait avec une unique corde : la carte croyait la
    ressource ponctuelle, et un fleuve pesait autant qu'un etang.

    Le tri se fait sur l'ECARTEMENT DES MILIEUX, et c'est ce choix qui decide
    de tout. Un lac rond rend une corde par angle de balayage, soixante en
    tout, dont les milieux tombent tous sur le centre : une seule ressource
    vue soixante fois, que l'ecartement ramene a une. Un estuaire de 30 km
    rend des milieux etales sur 30 km : autant de ressources reelles, toutes
    conservees. Un critere de recouvrement des couloirs, lui, aurait garde la
    rosette du lac rond, deux bandes de 60 m qui se croisent a 3 degres ne se
    recouvrant qu'a 7 pour cent.

    ECART_MIN_M joue le role du pas d'echantillonnage du trait de cote : une
    longue etendue d'eau vaut un point tous les tant de metres, parce qu'elle
    couvre effectivement cette distance.

    La plus longue course est acceptee sans condition : ne garder qu'elle
    redonne donc exactement l'ancien resultat, ce qui sert de test de
    non-regression.
    """
    eroded = poly.buffer(-width_m / 2.0)
    if eroded.is_empty:
        return []
    subs = list(eroded.geoms) if isinstance(eroded, MultiPolygon) else [eroded]

    # Chaque segment est ramene dans le repere d'origine des sa collecte. Le
    # balayage travaille dans un repere tourne propre a chaque angle ; comparer
    # des milieux d'un repere a l'autre n'aurait aucun sens.
    cand = []
    for part in subs:
        if part.is_empty or part.area <= 0:
            continue
        cx, cy = part.centroid.x, part.centroid.y
        for ang in np.arange(0, 180, angle_step):
            rot = affinity.rotate(part, -ang, origin=(cx, cy))
            rminx, rminy, rmaxx, rmaxy = rot.bounds
            step = max(width_m / 2.0, (rmaxy - rminy) / max_scan)
            y = rminy + step / 2.0
            while y <= rmaxy:
                inter = rot.intersection(LineString([(rminx - 10, y), (rmaxx + 10, y)]))
                if not inter.is_empty:
                    segs = [inter] if inter.geom_type == "LineString" else \
                           [s for s in getattr(inter, "geoms", []) if s.geom_type == "LineString"]
                    for s in segs:
                        if s.length >= Lmin:
                            cand.append((s.length,
                                         affinity.rotate(s, ang, origin=(cx, cy))))
                y += step
    if not cand:
        return []

    # Du plus long au plus court : la meilleure course de chaque secteur
    # s'installe la premiere, ses variantes voisines sont ecartees ensuite.
    cand.sort(key=lambda t: -t[0])
    ecart2 = ECART_MIN_M ** 2
    retenues, milieux = [], []
    for L, line in cand:
        (x1, y1), (x2, y2) = line.coords[0], line.coords[-1]
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        if any((mx - px) ** 2 + (my - py) ** 2 < ecart2 for px, py in milieux):
            continue
        milieux.append((mx, my))
        retenues.append((L, line))
    return retenues


def prefilter(poly, L):
    if poly.area < L * W * 0.9: return False
    b = poly.bounds
    return np.hypot(b[2] - b[0], b[3] - b[1]) >= L

# une seule passe geometrique : toutes les courses distinctes de chaque plan
# d'eau, classees ensuite par seuil. rang 1 = la plus longue, celle que
# l'ancienne version renvoyait seule.
t0 = time.time()
Lmin = min(SEUILS)
mesures = []
for ident, (p, ps, nm) in enumerate(zip(parts, parts_s, names)):
    if not prefilter(ps, Lmin): continue
    courses = toutes_courses(ps, W, Lmin)
    for rang, (l, line) in enumerate(courses, 1):
        mesures.append({"name": nm, "len": l, "line": line, "area": p.area,
                        "plan": ident, "rang": rang, "nb": len(courses)})
t_geo = time.time() - t0

# ---------- 4. sorties ----------
inv = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True)
feats = []
for m in mesures:
    seuil_max = max([s for s in SEUILS if m["len"] >= s], default=0)
    coords = [inv.transform(x, y) for x, y in m["line"].coords]
    feats.append({"type": "Feature",
        "geometry": {"type": "LineString",
                     "coordinates": [[round(x, 5), round(y, 5)] for x, y in coords]},
        "properties": {"nom": m["name"], "region": REGION,
                       "longueur_m": round(m["len"]), "aire_ha": round(m["area"] / 1e4, 1),
                       "seuil_max_m": seuil_max, "largeur_libre_m": W,
                       # plan_eau relie les courses d'une meme etendue. aire_ha
                       # est celle de l'etendue entiere et se repete donc sur
                       # chacune : pour totaliser une surface, ne sommer que
                       # les rang 1, sans quoi un fleuve compte n fois.
                       "plan_eau": m["plan"], "rang": m["rang"],
                       "nb_courses": m["nb"]}})

slug = REGION.lower().replace(" ", "-").replace("'", "")
out = f"{OUTDIR}/axes-ecopage-{slug}.geojson"
json.dump({"type": "FeatureCollection",
           "metadata": {"region": REGION,
               "source": "OpenStreetMap via Geofabrik",
               "methode": "recollage des polygones contigus, erosion de W/2, toutes les cordes inscrites dont les milieux sont ecartes d'au moins ECART_MIN_M",
               "largeur_libre_m": W,
               "ecart_min_m": ECART_MIN_M,
               "plusieurs_courses": "Un plan d'eau peut porter plusieurs courses : plan_eau les relie, rang 1 est la plus longue. aire_ha vaut pour l'etendue entiere et se repete sur chaque course ; pour totaliser une surface, ne sommer que les rang 1.",
               "avertissement": "profondeur, obstacles et degagement d'approche NON pris en compte : borne haute de candidats"},
           "features": feats},
          open(out, "w", encoding="utf-8"), ensure_ascii=False)

print(f"[{REGION}] {n_brut} polygones bruts -> {n} retenus -> {len(parts)} composantes recollees")
print(f"[{REGION}] temps : chargement {t_load:.0f}s | recollage {t_merge:.0f}s | geometrie {t_geo:.0f}s | TOTAL {time.time()-t_start:.0f}s")
for s in SEUILS:
    # "plans d'eau" = les rang 1, donc l'ancien decompte, seule base de
    # comparaison avec les fichiers de reference. "courses" = le total reel.
    tot = sum(1 for m in mesures if m["len"] >= s)
    r1  = sum(1 for m in mesures if m["len"] >= s and m["rang"] == 1)
    print(f"   L>={s:5} m, l>={W} m : {r1:5} plans d'eau, {tot:6} courses")
print(f"[{REGION}] ecrit : {out}")
