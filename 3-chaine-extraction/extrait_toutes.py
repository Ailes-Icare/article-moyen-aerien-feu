# -*- coding: utf-8 -*-
"""
Lance traite_region.py sur toutes les regions telechargees.

    python extrait_toutes.py                 toutes, 4 de front
    python extrait_toutes.py -j 1            en serie
    python extrait_toutes.py corse alsace    seulement celles-la
    python extrait_toutes.py --refaire       recalcule meme si le geojson existe

La liste des regions et la correspondance slug Geofabrik -> nom de region sont
lues dans telecharge_geofabrik.py : une seule table, pas deux a tenir a jour.

Deux points de conception.

REPRISE. Une region dont le geojson existe deja et se relit sans erreur est
sautee. Le calcul dure plus d'une heure au total ; il doit pouvoir etre
interrompu et repris sans tout refaire.

PARALLELISME PAR PROCESSUS. Chaque region est un processus separe, donc pas
de probleme de GIL ni d'etat partage. Le cout est en memoire : compter
quelques Go par region, d'ou le reglage par -j plutot qu'un nombre fige.
Le nom du slug de sortie est celui que traite_region.py calcule lui-meme,
REGION.lower() sans espaces ni apostrophes, pour que les fichiers produits
portent exactement le nom de ceux deja en place.
"""
import os, sys, time, json, subprocess
from concurrent.futures import ThreadPoolExecutor

ICI    = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "geofabirk")
# Meme variable que traite_region.py, sans quoi le pilote chercherait les
# resultats dans un dossier et les processus fils les ecriraient dans un
# autre : tout serait recalcule a chaque fois, ou tout serait saute a tort.
SORTIE = os.environ.get("AXES_OUTDIR") or os.path.join(ICI, "sorties-axes")
SCRIPT = os.path.join(ICI, "traite_region.py")

sys.path.insert(0, ICI)
from telecharge_geofabrik import REGIONS, humain          # table unique


def slug_sortie(nom_region):
    """Reproduit exactement le calcul de slug de traite_region.py."""
    return nom_region.lower().replace(" ", "-").replace("'", "")


def deja_calcule(chemin):
    """Vrai si le geojson existe et se relit : un fichier tronque est refait."""
    if not os.path.exists(chemin):
        return False
    try:
        with open(chemin, encoding="utf-8") as f:
            return "features" in json.load(f)
    except Exception:
        return False


def en_cours(slug):
    """Vrai si l'archive de la region est encore la, donc l'extraction en cours.

    Sans ce garde-fou, lancer ce script pendant que telecharge_geofabrik.py
    tourne pourrait lire un .shp a moitie ecrit : le fichier existe des le
    premier octet copie. telecharge_geofabrik.py n'efface l'archive qu'apres
    avoir verifie les dix fichiers, son absence est donc le seul signal sur
    lequel on puisse se fier.
    """
    z = os.path.join(RACINE, "_zip", slug + ".zip")
    return os.path.exists(z) or os.path.exists(z + ".part")


def traite(slug, nom):
    shp = os.path.join(RACINE, slug, "gis_osm_water_a_free_1.shp")
    out = os.path.join(SORTIE, "axes-ecopage-%s.geojson" % slug_sortie(nom))

    if en_cours(slug):
        return (nom, "EN COURS", 0, "telechargement non termine, a relancer ensuite")
    if not os.path.exists(shp):
        return (nom, "ABSENT", 0, "couche non telechargee : %s" % shp)
    if deja_calcule(out):
        return (nom, "SAUTE", 0, "geojson deja present")

    t0 = time.time()
    r = subprocess.run([sys.executable, SCRIPT, shp, nom],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    d = time.time() - t0
    if r.returncode != 0:
        detail = (r.stderr or r.stdout or "").strip().splitlines()
        return (nom, "ECHEC", d, detail[-1] if detail else "code %d" % r.returncode)
    return (nom, "OK", d, (r.stdout or "").strip())


def main():
    argv = sys.argv[1:]
    refaire = "--refaire" in argv
    j = 4
    if "-j" in argv:
        j = int(argv[argv.index("-j") + 1])
    noms = [a for a in argv if not a.startswith("-") and not a.isdigit()]

    voulues = REGIONS
    if noms:
        connus = {s for s, _ in REGIONS}
        inconnus = [a for a in noms if a not in connus]
        if inconnus:
            print("Region(s) inconnue(s) : %s" % ", ".join(inconnus))
            return 2
        voulues = [(s, n) for s, n in REGIONS if s in noms]

    os.makedirs(SORTIE, exist_ok=True)
    if refaire:
        for s, n in voulues:
            f = os.path.join(SORTIE, "axes-ecopage-%s.geojson" % slug_sortie(n))
            if os.path.exists(f):
                os.remove(f)

    print("%d region(s), %d processus de front\n" % (len(voulues), j))
    t0 = time.time()
    resultats = []
    with ThreadPoolExecutor(max_workers=j) as ex:
        for res in ex.map(lambda a: traite(*a), voulues):
            nom, etat, d, msg = res
            resultats.append(res)
            fait = len(resultats)
            if etat == "OK":
                # On ne garde que la ligne de comptage des axes, la plus utile.
                axes = [l.strip() for l in msg.splitlines() if "L>=  700" in l]
                print("[%2d/%2d] %-22s %s  %3.0f s   %s"
                      % (fait, len(voulues), nom, etat, d,
                         axes[0] if axes else ""))
            else:
                print("[%2d/%2d] %-22s %s  %s" % (fait, len(voulues), nom, etat, msg))

    duree = time.time() - t0
    ok = [r for r in resultats if r[1] == "OK"]
    print("\n" + "-" * 70)
    print("%d reussies, %d sautees, %d echecs, %d absentes  en %d min %02d s"
          % (len(ok),
             sum(1 for r in resultats if r[1] == "SAUTE"),
             sum(1 for r in resultats if r[1] == "ECHEC"),
             sum(1 for r in resultats if r[1] in ("ABSENT", "EN COURS")),
             duree // 60, duree % 60))

    # Recapitulatif du corpus produit, toutes regions confondues.
    total, poids = 0, 0
    for f in sorted(os.listdir(SORTIE)):
        if not f.endswith(".geojson"):
            continue
        p = os.path.join(SORTIE, f)
        poids += os.path.getsize(p)
        try:
            with open(p, encoding="utf-8") as fh:
                total += len(json.load(fh)["features"])
        except Exception:
            print("  illisible : %s" % f)
    print("%d axes au total dans %s (%s)" % (total, SORTIE, humain(poids)))
    return 1 if any(r[1] == "ECHEC" for r in resultats) else 0


if __name__ == "__main__":
    sys.exit(main())
