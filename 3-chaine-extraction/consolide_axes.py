# -*- coding: utf-8 -*-
"""
Consolidation nationale : 22 geojson regionaux -> plans-eau-france.json.

    python consolide_axes.py                          depuis sorties-axes-multi
    python consolide_axes.py sorties-axes             depuis un autre dossier
    python consolide_axes.py sorties-axes-multi sortie.json

Quatre etapes, chacune motivee.

1. DEDOUBLONNAGE INTER-REGIONS. Geofabrik livre les objets entiers, un plan
   d'eau a cheval sur deux regions est donc extrait des deux cotes. Mais le
   recollage differe : les polygones voisins hors region manquent, la
   composante n'est pas la meme, l'axe non plus. Les doublons se ressemblent
   sans etre identiques.

   Le critere retenu est physique : deux axes font double emploi si le milieu
   de l'un tombe SUR l'autre, a moins de 500 m, et qu'ils sont a peu pres
   paralleles. Il ne s'applique qu'entre deux fichiers regionaux differents,
   puisqu'a l'interieur d'un fichier l'extraction ne rend qu'un jeu de courses
   par composante : un doublon intra-region est impossible par construction.

   Ce critere est stable : de 100 m a 500 m de tolerance, le nombre de
   doublons ne bouge que de 103 a 106. C'est ce qui le distingue d'un reglage
   ajuste jusqu'a tomber sur le bon chiffre.

   Reserve honnete : le fichier historique annoncait 184 doublons retires, on
   en trouve ici environ 106. Le script d'origine est perdu et sa regle
   invisible ; a l'essai, une regle assez lache pour en retirer 184 fusionne
   aussi des etangs voisins distincts, a l'interieur d'une meme region. Le
   compte retenu ici est donc plus prudent, et l'ecart est assume.

2. AFFECTATION DEPARTEMENTALE. Le milieu de l'axe decide. Une tolerance de
   2 km rattrape l'imprecision du contour departemental, qui est simplifie :
   sans elle on perdrait des bassins portuaires et des etangs cotiers bien
   francais.

3. GLACIERS. L'extraction OSM prend les surfaces de glace pour des plans
   d'eau. On n'ecope pas sur un glacier. Seuls les noms COMMENCANT par le mot
   sont retires, pour ne pas emporter un lac qui le contiendrait par hasard.

4. HORS TERRITOIRE. Milieu a plus de 2 km de tout departement : lacs
   allemands, suisses, italiens, retenues espagnoles. Le Leman fait exception
   nommee, sa rive sud etant francaise.
"""
import io, os, re, sys, json, math, collections

ICI     = os.path.dirname(os.path.abspath(__file__))
HTML    = os.path.join(ICI, "plans-eau-ecopage.html")
ANCIEN  = os.path.join(ICI, "plans-eau-france.json")

SOURCE  = sys.argv[1] if len(sys.argv) > 1 else "sorties-axes-multi"
CIBLE   = sys.argv[2] if len(sys.argv) > 2 else "plans-eau-france.json"
SOURCE  = SOURCE if os.path.isabs(SOURCE) else os.path.join(ICI, SOURCE)
CIBLE   = CIBLE  if os.path.isabs(CIBLE)  else os.path.join(ICI, CIBLE)

RECOUV_KM   = 0.5     # milieu de l'un a moins de tant de l'axe de l'autre
PARALLELE   = 35.0    # ecart d'orientation tolere, en degres
TOLERANCE_KM = 2.0    # marge sur le contour departemental
GLACE = re.compile(r"^(ghiacciaio|glacier|glaciar|gletscher|nevero|vedretta)", re.I)
EXCEPTIONS = {"Le Léman"}

R = 6371.0


def xy(p, lat0):
    return (math.radians(p[0]) * R * math.cos(math.radians(lat0)),
            math.radians(p[1]) * R)


def km(a, b):
    return math.hypot((a[0] - b[0]) * 111.32 * math.cos(math.radians((a[1] + b[1]) / 2)),
                      (a[1] - b[1]) * 110.57)


def dist_pt_seg(p, a, b):
    """Distance en km d'un point au segment [a,b], en plan local."""
    lat0 = (a[1] + b[1]) / 2.0
    P, A, B = xy(p, lat0), xy(a, lat0), xy(b, lat0)
    vx, vy = B[0] - A[0], B[1] - A[1]
    wx, wy = P[0] - A[0], P[1] - A[1]
    L2 = vx * vx + vy * vy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, (wx * vx + wy * vy) / L2))
    return math.hypot(wx - t * vx, wy - t * vy)


def cap(a, b):
    """Orientation du segment, en degres, ramenee a [0,180)."""
    lat0 = (a[1] + b[1]) / 2.0
    A, B = xy(a, lat0), xy(b, lat0)
    return math.degrees(math.atan2(B[1] - A[1], B[0] - A[0])) % 180.0


def ecart_cap(c1, c2):
    d = abs(c1 - c2) % 180.0
    return min(d, 180.0 - d)


def milieu(ax):
    return ((ax["a"][0] + ax["b"][0]) / 2.0, (ax["a"][1] + ax["b"][1]) / 2.0)


# ------------------------------------------------------------------ lecture
fichiers = sorted(f for f in os.listdir(SOURCE) if f.endswith(".geojson"))
if len(fichiers) != 22:
    print("attention : %d fichiers regionaux au lieu de 22" % len(fichiers))

brut = []
for f in fichiers:
    d = json.load(io.open(os.path.join(SOURCE, f), encoding="utf-8"))
    for x in d["features"]:
        p, c = x["properties"], x["geometry"]["coordinates"]
        brut.append({"n": p["nom"], "l": p["longueur_m"], "ha": p["aire_ha"],
                     "a": [round(c[0][0], 4), round(c[0][1], 4)],
                     "b": [round(c[-1][0], 4), round(c[-1][1], 4)],
                     "_reg": f, "_plan": p.get("plan_eau"), "_rang": p.get("rang", 1)})
print("%d courses lues dans %d fichiers" % (len(brut), len(fichiers)))

# ------------------------------------------------- 1. dedoublonnage
# Du plus long au plus court : c'est l'axe le mieux mesure qui reste.
gr = collections.defaultdict(list)
gardes, n_dup = [], 0
for ax in sorted(brut, key=lambda z: -z["l"]):
    m = milieu(ax)
    c = cap(ax["a"], ax["b"])
    k = (round(m[0] / 0.2), round(m[1] / 0.2))
    double = False
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            for o in gr[(k[0] + dx, k[1] + dy)]:
                if o["_reg"] == ax["_reg"]:
                    continue
                if ecart_cap(c, o["_cap"]) > PARALLELE:
                    continue
                if dist_pt_seg(m, o["a"], o["b"]) <= RECOUV_KM:
                    double = True
                    break
            if double:
                break
        if double:
            break
    if double:
        n_dup += 1
    else:
        ax["_cap"] = c
        gr[k].append(ax)
        gardes.append(ax)
print("dedoublonnage : %d doublons inter-regions retires -> %d" % (n_dup, len(gardes)))

# ------------------------------------------------- 2. departements
DEPS = json.loads(re.search(r"^const DEPS\s*=\s*(\{.*?\});\s*$",
                            io.open(HTML, encoding="utf-8").read(), re.M | re.S).group(1))
RINGS = []
for f in DEPS["features"]:
    g = f["geometry"]
    anneaux = [g["coordinates"][0]] if g["type"] == "Polygon" else \
              [p[0] for p in g["coordinates"]] if g["type"] == "MultiPolygon" else []
    for r in anneaux:
        xs = [c[0] for c in r]
        ys = [c[1] for c in r]
        RINGS.append((min(xs), max(xs), min(ys), max(ys), r, f["properties"]["code"]))


def dedans(pt, ring):
    x, y = pt
    ok, j = False, len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi):
            ok = not ok
        j = i
    return ok


def departement(pt):
    """Code du departement contenant le point, sinon le plus proche a moins de
    TOLERANCE_KM, sinon None."""
    for x1, x2, y1, y2, r, code in RINGS:
        if x1 <= pt[0] <= x2 and y1 <= pt[1] <= y2 and dedans(pt, r):
            return code, 0.0
    best, bcode = 1e9, None
    for x1, x2, y1, y2, r, code in RINGS:
        if pt[0] < x1 - 1 or pt[0] > x2 + 1 or pt[1] < y1 - 1 or pt[1] > y2 + 1:
            continue
        for c in r:
            d = km(pt, c)
            if d < best:
                best, bcode = d, code
    return (bcode, best) if best <= TOLERANCE_KM else (None, best)


# ------------------------------------------------- 3 et 4. nettoyage
final, motifs = [], collections.Counter()
plans = {}
for ax in gardes:
    nom = ax["n"] or ""
    if GLACE.match(nom.strip()):
        motifs["glacier"] += 1
        continue
    m = milieu(ax)
    code, d = departement(m)
    if code is None:
        if nom in EXCEPTIONS:
            # Le Leman : milieu en eaux suisses, rive sud francaise. Rattache
            # a la Haute-Savoie, comme dans le fichier historique.
            code = "74"
            motifs["exception"] += 1
        else:
            motifs["hors territoire"] += 1
            continue
    cle = (ax["_reg"], ax["_plan"])
    plans.setdefault(cle, len(plans))
    final.append({"n": ax["n"], "l": ax["l"], "ha": ax["ha"], "d": code,
                  "a": ax["a"], "b": ax["b"],
                  "p": plans[cle], "r": ax["_rang"]})

final.sort(key=lambda z: -z["l"])
print("nettoyage : %s -> %d courses, %d plans d'eau"
      % (dict(motifs), len(final), len(plans)))

# ------------------------------------------------- ecriture
meta_src = {}
if os.path.exists(ANCIEN):
    meta_src = json.load(io.open(ANCIEN, encoding="utf-8"))

ecart = None
m0 = os.path.join(SOURCE, fichiers[0])
ecart = json.load(io.open(m0, encoding="utf-8"))["metadata"].get("ecart_min_m")

nb_plans = len(plans)
sortie = {
    "meta": {
        "titre": "Axes d'écopage mesurés sur les plans d'eau de France",
        "description": ("%d courses d'écopage réparties sur %d plans d'eau, extraites des "
                        "données Geofabrik/OSM par recollage des polygones contigus, érosion "
                        "de la moitié de la largeur requise et recherche de toutes les cordes "
                        "inscrites dont les milieux sont écartés d'au moins %s m. Bornes hautes "
                        "de candidats — la profondeur, les obstacles (ponts, câbles, lignes) et "
                        "le marnage estival ne sont pas pris en compte."
                        % (len(final), nb_plans, ecart)),
        "schema_axe": {"n": "nom", "l": "longueur exploitable (m)",
                       "ha": "surface du plan d'eau (ha), répétée sur chaque course",
                       "d": "département", "a": "extrémité 1 [lon,lat]",
                       "b": "extrémité 2 [lon,lat]",
                       "p": "identifiant du plan d'eau, commun aux courses d'une même étendue",
                       "r": "rang, 1 = la plus longue course de ce plan d'eau"},
        "plusieurs_courses": ("Une étendue peut porter plusieurs courses : p les relie, r les "
                              "ordonne. Pour totaliser une SURFACE, ne sommer que les r == 1, "
                              "sans quoi un fleuve compte autant de fois qu'il a de courses."),
        "largeur_libre_m": 60,
        "ecart_min_m": ecart,
        "nb_courses": len(final),
        "nb_plans_eau": nb_plans,
        "nb_courses_1000m": sum(1 for a in final if a["l"] >= 1000),
        "nb_courses_2000m": sum(1 for a in final if a["l"] >= 2000),
        "nb_departements": len({a["d"] for a in final}),
        "source": "extraction Geofabrik/OSM du 2026-08-17, consolidee par consolide_axes.py",
        "limites": meta_src.get("meta", {}).get("limites", ""),
        "dedoublonnage": ("%d doublons inter-regions retires. Critere : le milieu d'un axe "
                          "tombe a moins de %s km de l'autre axe, orientations ecartees de "
                          "moins de %s degres, et les deux viennent de fichiers regionaux "
                          "differents. Le fichier historique en annonçait 184 ; sa regle est "
                          "perdue, et toute regle assez lache pour en retirer autant fusionne "
                          "aussi des etangs voisins distincts au sein d'une meme region."
                          % (n_dup, RECOUV_KM, PARALLELE)),
        "nettoyage": ("%d surfaces de glace retirees (nom commençant par Glacier, Ghiacciaio, "
                      "Glaciar, Gletscher, Nevero ou Vedretta : on n'ecope pas sur un glacier), "
                      "%d courses hors territoire francais au-dela de %s km du contour "
                      "departemental." % (motifs["glacier"], motifs["hors territoire"], TOLERANCE_KM)),
        "exceptions": meta_src.get("meta", {}).get("exceptions", ""),
    },
    "axes": final,
    "adjacences": meta_src.get("adjacences", {}),
}
json.dump(sortie, io.open(CIBLE, "w", encoding="utf-8"), ensure_ascii=False)
print("ecrit : %s  (%.0f Ko)" % (CIBLE, os.path.getsize(CIBLE) / 1024))
