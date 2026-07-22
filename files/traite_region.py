#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Axes d'ecopage a partir d'un extrait Geofabrik (couche gis_osm_water_a_free_1).

    python3 traite_region.py <chemin.shp> <NomRegion> [seuils]

Sortie : GeoJSON des axes + une ligne de synthese par seuil (volontairement compact).
Concu pour survivre a un reset de conteneur : aucun etat externe, tout est recalcule.
"""
import sys, time, json, warnings
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
OUTDIR = "/mnt/user-data/outputs"

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

def prefilter(poly, L):
    if poly.area < L * W * 0.9: return False
    b = poly.bounds
    return np.hypot(b[2] - b[0], b[3] - b[1]) >= L

# une seule passe geometrique : on mesure l'axe max, on classe ensuite par seuil
t0 = time.time()
Lmin = min(SEUILS)
mesures = []
for p, ps, nm in zip(parts, parts_s, names):
    if not prefilter(ps, Lmin): continue
    l, line = longest_run(ps, W)
    if l >= Lmin:
        mesures.append({"name": nm, "len": l, "line": line, "area": p.area})
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
                       "seuil_max_m": seuil_max, "largeur_libre_m": W}})

slug = REGION.lower().replace(" ", "-").replace("'", "")
out = f"{OUTDIR}/axes-ecopage-{slug}.geojson"
json.dump({"type": "FeatureCollection",
           "metadata": {"region": REGION,
               "source": "OpenStreetMap via Geofabrik",
               "methode": "recollage des polygones contigus, erosion de W/2, plus longue corde inscrite",
               "largeur_libre_m": W,
               "avertissement": "profondeur, obstacles et degagement d'approche NON pris en compte : borne haute de candidats"},
           "features": feats},
          open(out, "w"), ensure_ascii=False)

print(f"[{REGION}] {n_brut} polygones bruts -> {n} retenus -> {len(parts)} composantes recollees")
print(f"[{REGION}] temps : chargement {t_load:.0f}s | recollage {t_merge:.0f}s | geometrie {t_geo:.0f}s | TOTAL {time.time()-t_start:.0f}s")
for s in SEUILS:
    print(f"   L>={s:5} m, l>={W} m : {sum(1 for m in mesures if m['len'] >= s):5} axes")
print(f"[{REGION}] ecrit : {out}")
