# -*- coding: utf-8 -*-
"""
Concept d'extraction tactique DFCI : Filtrage des plans d'eau pour écopage (L > 1500m)
Pré-requis : pip install geopandas shapely
"""
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon

def extraire_axe_majeur(geojson_input_path, output_json_path):
    print("Loading geographic dataset from Sandre (BD TOPAGE)...")
    # Chargement de la base brute (plusieurs centaines de Mo potentiels)
    gdf = gpd.read_file(geojson_input_path)
    
    # S'assurer d'être dans un système de projection métrique (ex: Lambert 93 - EPSG:2154)
    # indispensable pour calculer des distances réelles en mètres
    if gdf.crs.to_epsg() != 2154:
        gdf = gdf.to_crs(epsg=2154)
    
    liste_plans_eau = []
    
    print("Processing geometries and calculating maximum lengths...")
    for idx, row in gdf.iterrows():
        geom = row.geometry
        if geom is None:
            continue
            
        # Calcul de la boîte englobante orientée (Minimum Bounding Box)
        # L'axe le plus long de cette boîte donne la longueur maximale du plan d'eau
        obb = geom.minimum_rotated_rectangle
        
        # Extraction des sommets de la boîte englobante
        if isinstance(obb, Polygon):
            x, y = obb.exterior.coords.xy
            # Calcul des longueurs des côtés de la boîte
            side1 = ((x[0]-x[1])**2 + (y[0]-y[1])**2)**0.5
            side2 = ((x[1]-x[2])**2 + (y[1]-y[2])**2)**0.5
            longueur_max_metres = max(side1, side2)
            
            # Seuil de filtrage opérationnel : 1500 mètres
            if longueur_max_metres >= 1500:
                # Repasser le centroïde en coordonnées géographiques (WGS84 - EPSG:4326) pour D3.js
                centroid_wgs84 = gdf.loc[[idx]].to_crs(epsg=4326).geometry.centroid.values[0]
                
                liste_plans_eau.append({
                    "id": str(row.get("ID_POLYGON", idx)),
                    "nom": row.get("NOM_PLAN_EAU", row.get("nom", f"Plan d'eau {idx}")),
                    "longueur_m": round(longueur_max_metres, 1),
                    "lat": round(centroid_wgs84.y, 5),
                    "lon": round(centroid_wgs84.x, 5)
                })

    # Exportation au format standardisé JSON
    import json
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(liste_plans_eau, f, ensure_ascii=False, indent=2)
        
    print(f"Extraction terminée. {len(liste_plans_eau)} plans d'eau valides exportés dans {output_json_path}")

# Exemple d'exécution (décommenter en local)
# extraire_axe_majeur("PlanEau_FXX.shp", "plan-eau-france.json")