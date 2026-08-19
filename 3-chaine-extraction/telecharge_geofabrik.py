# -*- coding: utf-8 -*-
"""
Recuperation des couches d'eau Geofabrik pour les 22 regions metropolitaines.

    python telecharge_geofabrik.py                 toutes les regions
    python telecharge_geofabrik.py corse alsace    seulement celles-la
    python telecharge_geofabrik.py --garder-zip    ne supprime pas les archives

Pour chaque region : telechargement de l'archive shapefile, extraction des
seules couches utiles, rangement dans un sous-dossier, suppression du zip.

Trois partis pris qui meritent d'etre dits.

1. REPRISE. Le total avoisine 8 Go de telechargement ; une coupure reseau est
   probable. Une region deja extraite est donc sautee, et l'archive n'est
   effacee qu'apres verification que les cinq fichiers sont bien la. Le script
   peut etre relance autant de fois que necessaire sans rien recasser.

2. TELECHARGEMENT VERS UN FICHIER .part. Tant que le transfert n'est pas
   termine, l'archive porte l'extension .part. Une coupure ne laisse donc
   jamais un zip tronque qui passerait pour complet au lancement suivant.

3. DEUX COUCHES CONSERVEES, pas une. gis_osm_water_a_free_1 est la couche
   des SURFACES d'eau : c'est la seule que traite_region.py sait lire, il
   calcule des aires et erode les polygones. gis_osm_waterways_free_1 est la
   couche des LIGNES, les axes de cours d'eau, inutile au calcul actuel mais
   conservee pour le travail sur les embouchures : elle porte la ligne
   mediane des fleuves, exactement ce qu'il faut pour faire glisser une
   fenetre le long du cours. Elle ne coute que quelques dizaines de Mo face
   aux centaines du zip. Mettre COUCHES = ("gis_osm_water_a_free_1",) pour
   ne garder que le strict necessaire.

Aucune dependance : bibliotheque standard seule.
"""
import os, sys, time, zipfile, shutil, urllib.request, urllib.error

BASE   = "https://download.geofabrik.de/europe/france/%s-latest-free.shp.zip"
RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geofabirk")
TMP    = os.path.join(RACINE, "_zip")

# Affichage de la progression : seulement si l'on parle a un terminal.
TERMINAL = sys.stdout.isatty()

# Prefixes des couches conservees. Le "_a_" de water_a signifie "area" : c'est
# ce seul caractere qui separe les surfaces (utilisables) des lignes (non).
COUCHES = ("gis_osm_water_a_free_1", "gis_osm_waterways_free_1")

# Les cinq extensions qui forment un shapefile valide. Il en manque une et la
# couche est illisible, d'ou le controle explicite avant d'effacer l'archive.
EXTENSIONS = (".shp", ".shx", ".dbf", ".prj", ".cpg")

# Geofabrik decoupe la France selon les 22 anciennes regions, d'avant 2016.
# Deux libelles different de ceux du projet : "centre" y designe le
# Centre-Val de Loire, et PACA s'y ecrit en toutes lettres. La deuxieme
# colonne est le nom a passer en argument REGION a traite_region.py, pour que
# le geojson produit porte le meme slug que les fichiers deja en place.
REGIONS = [
    ("alsace",                     "Alsace"),
    ("aquitaine",                  "Aquitaine"),
    ("auvergne",                   "Auvergne"),
    ("basse-normandie",            "Basse-Normandie"),
    ("bourgogne",                  "Bourgogne"),
    ("bretagne",                   "Bretagne"),
    ("centre",                     "Centre-Val de Loire"),
    ("champagne-ardenne",          "Champagne-Ardenne"),
    ("corse",                      "Corse"),
    ("franche-comte",              "Franche-Comte"),
    ("haute-normandie",            "Haute-Normandie"),
    ("ile-de-france",              "Ile-de-France"),
    ("languedoc-roussillon",       "Languedoc-Roussillon"),
    ("limousin",                   "Limousin"),
    ("lorraine",                   "Lorraine"),
    ("midi-pyrenees",              "Midi-Pyrenees"),
    ("nord-pas-de-calais",         "Nord-Pas-de-Calais"),
    ("pays-de-la-loire",           "Pays de la Loire"),
    ("picardie",                   "Picardie"),
    ("poitou-charentes",           "Poitou-Charentes"),
    ("provence-alpes-cote-d-azur", "PACA"),
    ("rhone-alpes",                "Rhone-Alpes"),
]
# Les collectivites d'outre-mer sont volontairement absentes : les outils du
# projet ne traitent que la metropole.


def humain(n):
    for u in ("o", "Ko", "Mo", "Go"):
        if n < 1024 or u == "Go":
            return "%.1f %s" % (n, u)
        n /= 1024.0


def deja_fait(dossier):
    """Vrai si les couches demandees sont completes dans le dossier."""
    if not os.path.isdir(dossier):
        return False
    for c in COUCHES:
        for e in EXTENSIONS:
            if not os.path.exists(os.path.join(dossier, c + e)):
                return False
    return True


def telecharge(url, cible, essais=3):
    """Telecharge vers cible.part puis renomme. Retourne la taille obtenue."""
    part = cible + ".part"
    for tentative in range(1, essais + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "article-feu/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                total = int(r.headers.get("Content-Length") or 0)
                lu, t0, dernier = 0, time.time(), 0.0
                with open(part, "wb") as f:
                    while True:
                        bloc = r.read(1 << 20)
                        if not bloc:
                            break
                        f.write(bloc)
                        lu += len(bloc)
                        maintenant = time.time()
                        # Progression seulement en terminal : redirigee dans un
                        # fichier, la reecriture par \r laisse une bouillie de
                        # lignes accolees au lieu d'une barre qui s'efface.
                        if TERMINAL and maintenant - dernier > 2.0:
                            dernier = maintenant
                            vitesse = lu / max(maintenant - t0, 1e-6)
                            pct = (" %5.1f%%" % (100.0 * lu / total)) if total else ""
                            sys.stdout.write("\r      %s%s  %s/s   "
                                             % (humain(lu), pct, humain(vitesse)))
                            sys.stdout.flush()
            if TERMINAL:
                sys.stdout.write("\r" + " " * 60 + "\r")
            if total and lu != total:
                raise IOError("archive tronquee : %d octets sur %d" % (lu, total))
            os.replace(part, cible)
            return lu
        except (urllib.error.URLError, IOError, OSError) as e:
            if os.path.exists(part):
                os.remove(part)
            if tentative == essais:
                raise
            attente = 5 * tentative
            print("      echec (%s), nouvel essai dans %d s" % (e, attente))
            time.sleep(attente)


def extrait(zip_path, dossier):
    """Extrait les seules couches voulues. Retourne la liste des fichiers."""
    os.makedirs(dossier, exist_ok=True)
    poses = []
    with zipfile.ZipFile(zip_path) as z:
        for nom in z.namelist():
            base = os.path.basename(nom)
            if not base or not base.startswith(COUCHES):
                continue
            # On ecrit a plat : l'archive Geofabrik peut nicher les fichiers,
            # traite_region.py attend un chemin direct vers le .shp.
            with z.open(nom) as src, open(os.path.join(dossier, base), "wb") as dst:
                shutil.copyfileobj(src, dst, 1 << 20)
            poses.append(base)
    return poses


def complet(dossier, poses):
    """Verifie qu'aucune extension ne manque avant d'effacer l'archive."""
    manquants = []
    for c in COUCHES:
        for e in EXTENSIONS:
            if c + e not in poses:
                manquants.append(c + e)
    return manquants


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    garder = "--garder-zip" in sys.argv

    voulues = REGIONS
    if args:
        connus = {s for s, _ in REGIONS}
        inconnus = [a for a in args if a not in connus]
        if inconnus:
            print("Region(s) inconnue(s) : %s" % ", ".join(inconnus))
            print("Attendu parmi : %s" % ", ".join(s for s, _ in REGIONS))
            return 2
        voulues = [(s, n) for s, n in REGIONS if s in args]

    os.makedirs(TMP, exist_ok=True)
    t_debut = time.time()
    faits, sautes, echecs, octets = [], [], [], 0

    for i, (slug, nom) in enumerate(voulues, 1):
        dossier = os.path.join(RACINE, slug)
        print("[%2d/%2d] %s" % (i, len(voulues), nom))

        if deja_fait(dossier):
            print("      deja present, saute")
            sautes.append(slug)
            continue

        zip_path = os.path.join(TMP, slug + ".zip")
        try:
            if not os.path.exists(zip_path):
                taille = telecharge(BASE % slug, zip_path)
                octets += taille
                print("      telecharge : %s" % humain(taille))
            else:
                print("      archive deja la, extraction directe")

            poses = extrait(zip_path, dossier)
            manquants = complet(dossier, poses)
            if manquants:
                # On garde l'archive : sans elle, impossible de rattraper.
                raise IOError("fichiers absents de l'archive : %s" % ", ".join(manquants))

            tailles = sum(os.path.getsize(os.path.join(dossier, f)) for f in poses)
            print("      extrait    : %d fichiers, %s" % (len(poses), humain(tailles)))

            if not garder:
                os.remove(zip_path)
                print("      archive supprimee")
            faits.append(slug)

        except Exception as e:
            print("      ECHEC : %s" % e)
            echecs.append((slug, str(e)))

    duree = time.time() - t_debut
    print("\n%s" % ("-" * 58))
    print("%d region(s) traitee(s), %d sautee(s), %d en echec"
          % (len(faits), len(sautes), len(echecs)))
    print("%s telecharges en %d min %02d s" % (humain(octets), duree // 60, duree % 60))
    for slug, msg in echecs:
        print("  echec %s : %s" % (slug, msg))
    if echecs:
        print("\nRelancez le script : les regions reussies seront sautees.")

    if faits or sautes:
        print("\nPour lancer l'extraction des axes sur une region :")
        s, n = (faits + sautes)[0], dict(REGIONS)[(faits + sautes)[0]]
        print('  python traite_region.py "%s" "%s"'
              % (os.path.join(RACINE, s, "gis_osm_water_a_free_1.shp"), n))
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
