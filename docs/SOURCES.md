# Plot — Sources de données open data

Toutes les sources ci-dessous sont **gratuites, Licence Ouverte 2.0**, sans clé API (sauf mention).

---

## 1. Cadastre (parcelles, limites, surfaces)

| Source | Usage | URL |
|---|---|---|
| **API Carto — Cadastre** | Parcelle par ID, par zone, par geom | `https://apicarto.ign.fr/api/cadastre/parcelle` |
| **Géoplateforme WFS** | Requêtes spatiales (bbox, CQL) | `https://data.geopf.fr/wfs/ows` |
| **Étalab bulk** | Download GeoJSON complet par département | `https://cadastre.data.gouv.fr/data/etalab-cadastre/` |

**Champs clés retournés** : `idu` (ID parcelle 14 car.), `contenance` (surface m²), `geometry` (MultiPolygon WGS84), `code_insee`, `section`, `numero`

**Exemple** :
```
https://apicarto.ign.fr/api/cadastre/parcelle?code_insee=44109&section=EX&numero=0080
```

---

## 2. DVF — Transactions immobilières

| Source | Usage | URL |
|---|---|---|
| **Geo-DVF** | Transactions géolocalisées par année/département | `https://files.data.gouv.fr/geo-dvf/latest/csv/{YEAR}/{DEPT}.csv.gz` |
| **Statistiques DVF** | Prix m² moyen/médian par commune | `https://www.data.gouv.fr/datasets/statistiques-dvf` |
| **VALORIS API** | REST — prix médian par commune | `https://www.valoris-immo.fr/api/v1/prix-median` |
| **DVF+ (Cerema)** | Données enrichies, géomutations | `https://www.data.gouv.fr/datasets/dvf-open-data` |

**Exemple Geo-DVF** :
```
https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/75.csv.gz
```

⚠️ DVF exclut Alsace-Moselle et Mayotte.

---

## 3. PLU / PLUi — Zones constructibles

| Source | Usage | URL |
|---|---|---|
| **API Carto — GPU** | Zone urba par géométrie | `https://apicarto.ign.fr/api/gpu/zone-urba` |
| **GPU API** | Documents PLU, téléchargement règlements | `https://www.geoportail-urbanisme.gouv.fr/api/` |
| **Zones PLU France** | GeoParquet national complet | `https://www.data.gouv.fr/datasets/zones-plu-france` |

**Champs clés** : `libelle` (Uc, etc.), `destdomi` (vocation), `urlfic` (règlement PDF)

**Exemple** :
```
https://apicarto.ign.fr/api/gpu/zone-urba?geom={"type":"Point","coordinates":[2.35,48.85]}&insee=75056
```

---

## 4. Altimétrie / MNT (pente, exposition)

| Source | Usage | URL |
|---|---|---|
| **IGN Altimétrie REST** | Altitude d'un point ou profil | `https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json` |
| **RGE ALTI®** | MNT 1m/5m (download ou WMTS) | `https://cartes.gouv.fr/catalogue/dataset/IGNF_RGE-ALTI` |
| **LiDAR HD** | MNT haute résolution 1m | Via cartes.gouv.fr |

**Exemple** — altitude d'un point :
```
https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon=2.35&lat=48.85&resource=ign_rge_alti_wld
```

**Calcul pente/exposition** : échantillonner une grille de points autour de la parcelle, calculer le gradient localement.

---

## 5. Risques naturels (Georisque / BRGM)

| Source | Usage | URL |
|---|---|---|
| **API Géorisques** | Argiles, radon, inondation, séisme, PPR | `https://georisques.gouv.fr/api/v1/` |

**Endpoints** :
| Risque | Endpoint |
|---|---|
| Argiles (retrait-gonflement) | `/api/v1/argiles` |
| Radon | `/api/v1/radon` |
| Inondation (AZI) | `/api/v1/azi` |
| PPR | `/api/v1/ppr` |
| Cavités souterraines | `/api/v1/cavites` |
| Mouvements de terrain | `/api/v1/mvt` |
| Sismicité | `/api/v1/zonage_sismique` |
| CATNAT historique | `/api/v1/catnat` |
| Rapport complet (JSON) | `/api/v1/resultats_rapport_risque` |

**Exemple** :
```
https://georisques.gouv.fr/api/v1/argiles?code_insee=75056
```

---

## 6. Transport / POI / Géocodage

| Source | Usage | URL |
|---|---|---|
| **IGN Géocodage** | Adresse → coordonnées | `https://data.geopf.fr/geocodage/search` |
| **IGN Géocodage inverse** | Coordonnées → adresse | `https://data.geopf.fr/geocodage/reverse` |
| **IGN Itinéraire** | Distance/temps trajet | `https://data.geopf.fr/navigation/itineraire` |
| **IGN Isochrone** | Zones d'accessibilité | `https://data.geopf.fr/navigation/isochrone` |
| **Overpass API** | POI OSM (écoles, commerces, transport) | `https://overpass-api.de/api/interpreter` |

---

## 7. Eau souterraine (nappe phréatique)

| Source | Usage | URL |
|---|---|---|
| **Hub'Eau Piézométrie** | Stations piézomètres, niveaux nappe | `https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/` |

**Endpoints** :
- `/stations` — liste des stations
- `/chroniques` — séries temporelles (niveau nappe)
- `/chroniques_tr` — données temps réel (~1500 capteurs)

**Exemple** :
```
https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?code_commune=62193&format=json
```

---

## 8. DPE — Diagnostic énergétique

| Source | Usage | URL |
|---|---|---|
| **ADEME API (data-fair)** | 15.4M de DPE, filter par commune/adresse | `https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines` |
| **ADEME dump SQL** | Bulk PostgreSQL complet | `https://opendata.ademe.fr/dump_dpev2_prod_fdld.sql.gz` |

**Champs clés** : `etiquette_dpe` (A-G), `conso_5_usages_par_m2_ep`, `adresse_ban`, `code_postal_ban`, `_geopoint`, `surface_habitable_immeuble`

**Exemple** — DPE d'une adresse :
```
https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines?q=25+Rue+de+Belfort+Carcassonne&select=numero_dpe,adresse_ban,etiquette_dpe
```

⚠️ Pas de référence cadastrale dans les données DPE → join spatial via `_geopoint` + parcelle cadastre.

---

## 9. Loyers — Marché locatif

| Source | Usage | URL |
|---|---|---|
| **Carte des loyers** | Loyer €/m² par commune (ANIL) | `https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune` |
| **OLL** | Observatoires Locaux des Loyers | `https://www.data.gouv.fr/fr/organizations/observatoires-locaux-des-loyers/` |
| **Encadrement Paris** | Loyers encadrés par quartier | `https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/` |

---

## 10. Taxe foncière

| Source | Usage | URL |
|---|---|---|
| **REI (DGFiP)** | Bases, taux, produits par commune | `https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4` |
| **Fiscalité locale Géo** | Taux votés par commune (TFPB, TH, etc.) | `https://www.data.gouv.fr/datasets/fiscalite-locale-des-particuliers-geo` |
| **impots.gouv.fr stats** | Taux votés XLSX | `https://www.impots.gouv.fr/statistiques-collectivites-locales` |

---

## Résumé rapide

| Besoin | Source principale | Endpoint |
|---|---|---|
| Parcelles | API Carto cadastre | `apicarto.ign.fr/api/cadastre/parcelle` |
| Transactions | Geo-DVF | `files.data.gouv.fr/geo-dvf/latest/csv/` |
| Prix m² | Statistiques DVF | `data.gouv.fr/datasets/statistiques-dvf` |
| Zones constructibles | API Carto GPU | `apicarto.ign.fr/api/gpu/zone-urba` |
| Pente / exposition | IGN Altimétrie | `data.geopf.fr/altimetrie/...` |
| Risques naturels | Géorisques | `georisques.gouv.fr/api/v1/` |
| Transport / POI | IGN + OSM | `data.geopf.fr/geocodage` + Overpass |
| Eau souterraine | Hub'Eau | `hubeau.eaufrance.fr/api/v1/niveaux_nappes/` |
| DPE | ADEME | `data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/` |
| Loyers | Carte des loyers | `data.gouv.fr/datasets/carte-des-loyers` |
| Taxe foncière | REI DGFiP | `data.gouv.fr/datasets/...rei-4` |
