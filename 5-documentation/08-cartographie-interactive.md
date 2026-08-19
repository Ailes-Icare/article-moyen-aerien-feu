# Cartographie prospective de l'aléa feux de forêt & réseau des pélicandromes

**Fichier** : [`1-outils/pelicandromes/cartographie-interactive-v18.html`](../1-outils/pelicandromes/cartographie-interactive-v18.html)
**À charger** : `chronologie-pelicandromes_4_1.json`
**Facultatif** : `carte2-data-v2.json`

Deux cartes dans une seule page. La première montre **où le feu risque de se
déplacer** dans les décennies qui viennent ; la seconde superpose ce risque au
**réseau des pélicandromes** existant.

---

## La première carte — l'aléa projeté

Elle montre l'extension attendue des zones sensibles au feu, avec des couches
que l'on active séparément : l'allongement de la saison des feux à l'horizon
2090, l'émergence d'une troisième zone dans le Centre-Ouest, l'élargissement
des deux zones historiques.

Le fond documentaire est le rapport interministériel de 2010 sur le changement
climatique et l'extension des zones sensibles, et les projections Météo-France
associées.

---

## La seconde carte — le risque par territoire

Elle colore les départements et les arrondissements selon leur fréquence de feu
attendue, et laisse voir par-dessus les pélicandromes qui les desservent.

### Le système de couleurs en poupée russe

`carte2-data-v2.json` associe un code géographique à une couleur. Le principe
est simple et puissant : **vous n'êtes pas obligé de renseigner tous les
arrondissements**.

```json
{
  "33":    "#f97316",
  "33001": "#991b1b"
}
```

Ici toute la Gironde est orange, **sauf** l'arrondissement de Blaye, en rouge
foncé. Une valeur départementale sert de fond, une valeur d'arrondissement la
recouvre localement.

### Le piège des codes

Les codes d'arrondissement sont les **codes INSEE à 5 caractères**, pas des
codes à 3 chiffres. Blaye est `33001`, Bordeaux `33002`, Bastia `2B002`.

Une documentation ancienne mentionnait `331`, `332` : c'est faux, et les
dérogations écrites ainsi ne s'appliqueraient jamais — silencieusement, sans
message d'erreur.

### L'échelle à quatre niveaux

| Couleur | Fréquence |
|---|---|
| `#FDF2F2` | exceptionnelle — moins d'une fois par décennie |
| `#EAB308` | peu fréquente — 1 à 2 fois par décennie |
| `#F97316` | fréquente — 3 à 5 fois par décennie |
| `#991B1B` | très fréquente — plus de 5 fois par décennie |

---

## Comment les données de risque ont été obtenues

Point important pour qui voudrait citer ces couleurs.

La donnée d'origine est une **grille climatique**, pas une table
administrative : il n'existe aucune donnée officielle « par arrondissement »
derrière cette carte. Les valeurs de `carte2-data-v2.json` ont été obtenues en
géoréférençant la figure publiée puis en échantillonnant la classe dominante de
chaque arrondissement.

C'est une **interprétation reproductible**, assumée comme telle. Deux réserves
de confiance sont à connaître : la moitié nord, où le moutonnement fin
orange/jaune rend la classe majoritaire parfois limite, et les arrondissements
minuscules ou côtiers, où l'échantillon est maigre.

Pour une version fondée sur des grilles téléchargeables plutôt que sur la
relecture d'une image, la piste propre est le portail DRIAS-Climat.

---

## Les filtres d'affichage

Une section *Afficher sur les cartes* permet de cocher ou décocher chaque
catégorie de site — fermés, en construction, mobiles, production. Utile pour
produire une image qui ne montre que le réseau actif, ou au contraire seulement
ce qui a disparu.

---

## Les versions antérieures

`cartographie-interactive-v13.html` et `v16_1.html` sont dans les archives.
Elles précèdent des corrections de données du réseau : des sites y sont classés
« utilisation limitée » alors qu'ils sont fermés de fait, et le site de
production n'y figure pas.
