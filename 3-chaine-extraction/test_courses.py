# -*- coding: utf-8 -*-
"""
Banc de test de toutes_courses, sur formes dont la reponse est connue.

Les trois premiers cas viennent du controle d'origine de longest_run : ils
verifient que le rang 1 n'a pas bouge, c'est-a-dire qu'on n'a rien casse.
Les suivants verifient le comportement nouveau, celui qui distingue une
ressource ponctuelle d'une ressource etalee.

    python test_courses.py
"""
import sys, os, importlib.util
from shapely.geometry import Polygon, Point

ICI = os.path.dirname(os.path.abspath(__file__))

# traite_region.py s'execute de bout en bout a l'import : on charge le module
# en lui donnant un argv complet mais un shapefile inexistant, ce qui echoue
# proprement APRES la definition des fonctions... non : il echouerait avant.
# On relit donc le fichier et on n'execute que ce qui precede le chargement.
src = open(os.path.join(ICI, "traite_region.py"), encoding="utf-8").read()
coupe = src.index("t_start = time.time()")
entete = src[:coupe]
# Le corps du script commence apres ; les fonctions sont plus bas, on les
# recupere en isolant leurs definitions.
deb = src.index("def longest_run")
fin = src.index("# une seule passe geometrique")
code = entete + "\n" + src[deb:fin]

ns = {"__name__": "traite_region_fonctions",
      "__file__": os.path.join(ICI, "traite_region.py")}
sys.argv = ["traite_region.py", "inexistant.shp", "Test"]
exec(compile(code, "traite_region.py", "exec"), ns)

toutes_courses = ns["toutes_courses"]
longest_run    = ns["longest_run"]
ECART          = ns["ECART_MIN_M"]

echecs = []


def verifie(titre, obtenu, attendu, tol=0):
    ok = abs(obtenu - attendu) <= tol
    print("  %-58s %8s  (attendu %s%s)  %s"
          % (titre, obtenu, attendu, " +/-%d" % tol if tol else "",
             "OK" if ok else "ECHEC"))
    if not ok:
        echecs.append(titre)


def rect(L, l):
    return Polygon([(0, 0), (L, 0), (L, l), (0, l)])


print("ECART_MIN_M = %d m\n" % ECART)
print("--- non-regression : le rang 1 doit valoir l'ancien resultat ---")

# Rectangle 2000 x 300, largeur libre 100 : erosion de 50 par bord, il reste
# 1900 x 200. La plus longue corde vaut donc 1900 m, mesuree 1903 par le
# balayage a 3 degres. C'est la valeur du controle d'origine.
c = toutes_courses(rect(2000, 300), 100, 700)
verifie("rect 2000x300, largeur 100 : rang 1", round(c[0][0]), 1903, tol=8)
verifie("rect 2000x300 : longest_run d'origine",
        round(longest_run(rect(2000, 300), 100)[0]), round(c[0][0]), tol=0)

# Rectangle 2000 x 80 : 80 < 100, l'erosion vide le polygone. Aucune course.
verifie("rect 2000x80, largeur 100 : trop etroit",
        len(toutes_courses(rect(2000, 80), 100, 700)), 0)

# Disque de rayon 800, largeur 100 : erode en rayon 750, diametre 1500.
d = toutes_courses(Point(0, 0).buffer(800, resolution=64), 100, 700)
verifie("disque r=800, largeur 100 : rang 1", round(d[0][0]), 1500, tol=15)

print("\n--- comportement nouveau : ponctuel contre etale ---")

# Le disque est la ressource ponctuelle par excellence : toutes ses cordes
# passent par le centre, leurs milieux sont confondus. Une seule course.
verifie("disque r=800 : nombre de courses", len(d), 1)

# Un rectangle de 30 km sur 300 m est l'estuaire schematique.
e = toutes_courses(rect(30000, 300), 100, 700)
verifie("rect 30000x300 : rang 1 = toute la longueur", round(e[0][0]), 29900, tol=120)

# Combien de courses ? Pas un chiffre devine. Le balayage produit des milieux
# espaces d'environ ECART/sin(pas d'angle) ; quand cet espacement passe juste
# sous le seuil, un candidat sur deux tombe. Le nombre retenu est donc encadre,
# pas determine : entre une course tous les deux ECART et une tous les ECART.
bas, haut = 30000 // (2 * ECART), 30000 // ECART + 2
verifie("rect 30000x300 : nombre de courses dans [%d, %d]" % (bas, haut),
        1 if bas <= len(e) <= haut else 0, 1)
print("        (%d courses retenues, soit un point tous les %.1f km)"
      % (len(e), 30.0 / max(len(e), 1)))

# L'invariant qui compte vraiment : les courses doivent s'ETALER sur toute la
# longueur, pas s'agglutiner au milieu. C'est la difference entre une ressource
# etalee et une ressource ponctuelle, donc tout l'objet de la modification.
xs = [(f[1].coords[0][0] + f[1].coords[-1][0]) / 2.0 for f in e]
etendue = (max(xs) - min(xs)) / 29900.0
verifie("rect 30000x300 : les milieux couvrent >= 80%% de la longueur",
        1 if etendue >= 0.80 else 0, 1)
print("        (etendue reelle des milieux : %.0f %% de la longueur)" % (100 * etendue))

# Les milieux retenus doivent bien etre ecartes : c'est l'invariant du tri.
pires = 1e18
for i in range(len(e)):
    (ax1, ay1), (ax2, ay2) = e[i][1].coords[0], e[i][1].coords[-1]
    for j in range(i + 1, len(e)):
        (bx1, by1), (bx2, by2) = e[j][1].coords[0], e[j][1].coords[-1]
        dx = (ax1 + ax2) / 2 - (bx1 + bx2) / 2
        dy = (ay1 + ay2) / 2 - (by1 + by2) / 2
        pires = min(pires, (dx * dx + dy * dy) ** 0.5)
verifie("rect 30000x300 : ecart minimal entre milieux",
        int(pires), ECART, tol=ECART)          # jamais en dessous, verifie ci-dessous
if pires < ECART - 1:
    echecs.append("invariant d'ecartement viole : %.0f m < %d m" % (pires, ECART))
    print("  INVARIANT VIOLE : deux milieux a %.0f m alors que le seuil est %d m"
          % (pires, ECART))

# Les courses sont rendues de la plus longue a la plus courte.
verifie("rect 30000x300 : rang 1 est bien le plus long",
        1 if all(e[i][0] >= e[i + 1][0] for i in range(len(e) - 1)) else 0, 1)

print()
if echecs:
    print("%d ECHEC(S) : %s" % (len(echecs), " | ".join(echecs)))
    sys.exit(1)
print("tous les controles passent")
