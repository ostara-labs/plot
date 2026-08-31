# Plot — Sources de données open data

Toutes les sources ci-dessous sont **gratuites**, en **Licence Ouverte 2.0** (sauf mention), sans clé API (sauf mention explicite).

---

## 1. Cadastre (parcelles, limites, surfaces)

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **API Carto — Cadastre** | Parcelle par ID, par zone, par geom | `https://apicarto.ign.fr/api/cadastre/parcelle` | `https://apicarto.ign.fr/api/doc/cadastre` |
| **Géoplateforme WFS** | Requêtes spatiales (bbox, CQL) | `https://data.geopf.fr/wfs/ows` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/diffusion` |
| **Étalab bulk** | Download GeoJSON complet par département | `https://cadastre.data.gouv.fr/data/etalab-cadastre/` | `https://cadastre.data.gouv.fr/` |

**Champs clés retournés** : `idu` (ID parcelle 14 car.), `contenance` (surface m²), `geometry` (MultiPolygon WGS84), `code_insee`, `section`, `numero`

**Exemple** :
```
https://apicarto.ign.fr/api/cadastre/parcelle?code_insee=44109&section=EX&numero=0080
```

---

## 2. DVF — Transactions immobilières

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **Geo-DVF** | Transactions géolocalisées par année/département | `https://files.data.gouv.fr/geo-dvf/latest/csv/{YEAR}/{DEPT}.csv.gz` | `https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/` |
| **Statistiques DVF** | Prix m² moyen/médian par commune | `https://www.data.gouv.fr/datasets/statistiques-dvf` | `https://www.data.gouv.fr/datasets/statistiques-dvf` |
| **VALORIS API** | REST — prix médian par commune | `https://www.valoris-immo.fr/api/v1/prix-median` | `https://www.valoris-immo.fr/api/v1/docs` |
| **DVF+ (Cerema)** | Données enrichies, géomutations | `https://www.data.gouv.fr/datasets/dvf-open-data` | `https://www.data.gouv.fr/datasets/dvf-open-data` |

**Exemple Geo-DVF** :
```
https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/75.csv.gz
```

⚠️ DVF exclut Alsace-Moselle et Mayotte.

---

## 3. PLU / PLUi — Zones constructibles

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **API Carto — GPU** | Zone urba par géométrie | `https://apicarto.ign.fr/api/gpu/zone-urba` | `https://apicarto.ign.fr/api/doc/gpu` |
| **GPU API** | Documents PLU, téléchargement règlements | `https://www.geoportail-urbanisme.gouv.fr/api/` | `https://www.geoportail-urbanisme.gouv.fr/api/` |
| **Zones PLU France** | GeoParquet national complet | `https://www.data.gouv.fr/datasets/zones-plu-france` | `https://www.data.gouv.fr/datasets/zones-plu-france` |

**Champs clés** : `libelle` (Uc, etc.), `destdomi` (vocation), `urlfic` (règlement PDF)

**Exemple** :
```
https://apicarto.ign.fr/api/gpu/zone-urba?geom={"type":"Point","coordinates":[2.35,48.85]}&insee=75056
```

---

## 4. Altimétrie / MNT (pente, exposition)

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **IGN Altimétrie REST** | Altitude d'un point ou profil | `https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/altimetrie` |
| **RGE ALTI®** | MNT 1m/5m (download ou WMTS) | `https://cartes.gouv.fr/catalogue/dataset/IGNF_RGE-ALTI` | `https://geoservices.ign.fr/documentation/donnees/alti/rgealti` |
| **LiDAR HD** | MNT haute résolution 1m | Via cartes.gouv.fr | `https://geoservices.ign.fr/lidarhd` |

**Exemple** — altitude d'un point :
```
https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon=2.35&lat=48.85&resource=ign_rge_alti_wld
```

**Calcul pente/exposition** : échantillonner une grille de points autour de la parcelle, calculer le gradient localement.

---

## 5. Risques naturels (Georisque / BRGM)

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **API Géorisques** | Argiles, radon, inondation, séisme, PPR | `https://georisques.gouv.fr/api/v1/` | `https://www.georisques.gouv.fr/doc-api` |

**Endpoints V1** :
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
| Feux de forêt (zonage) | `/api/v1/risques` (risque `FEUFORET`) |
| OLD (obligations débroussaillement) | `/api/v1/old` |
| Rapport complet (JSON) | `/api/v1/resultats_rapport_risque` |

**Exemple** :
```
https://georisques.gouv.fr/api/v1/argiles?code_insee=75056
```

### API Géorisques V2 — par parcelle cadastrale ⭐

L'**API V2** (doc : `https://www.georisques.gouv.fr/doc-api`) accepte `codesParcelle` + `rayon` (mètres), `geometry` (WKT), `longitude`/`latitude`, `codesInsee` — c'est le mode d'interrogation idéal pour le scoring par parcelle. Token **gratuit** (Cerbère/FranceConnect, validité 1 an) envoyé en header `X-API-Key`. Rate limit : 1000 req/min/IP.

| Endpoint | Contenu |
|---|---|
| `/api/v2/installations_nucleaires` | Installations nucléaires de base (INB) |
| `/api/v2/installations_classees` | ICPE + filtre `statutSeveso` (SEUIL_HAUT/SEUIL_BAS) |
| `/api/v2/ssp` | Sites et sols pollués (SIS/BASOL) + `/casias` + `/conclusions_sis` |
| `/api/v2/cavites` | Cavités souterraines (carrières, caves, marnières) |
| `/api/v2/gaspar/pprm` | Plans de Prévention des Risques Miniers |

---

## 6. Transport / POI / Géocodage

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **IGN Géocodage** | Adresse → coordonnées | `https://data.geopf.fr/geocodage/search` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage` |
| **IGN Géocodage inverse** | Coordonnées → adresse | `https://data.geopf.fr/geocodage/reverse` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage` |
| **IGN Itinéraire** | Distance/temps trajet | `https://data.geopf.fr/navigation/itineraire` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/itineraire` |
| **IGN Isochrone** | Zones d'accessibilité | `https://data.geopf.fr/navigation/isochrone` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/isochrone` |
| **Overpass API** | POI OSM (écoles, commerces, transport) | `https://overpass-api.de/api/interpreter` | `https://wiki.openstreetmap.org/wiki/Overpass_API` |

---

## 7. Eau souterraine (nappe phréatique)

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **Hub'Eau Piézométrie** | Stations piézomètres, niveaux nappe | `https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/` | `https://hubeau.eaufrance.fr/page/api-piezometrie` |

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

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **ADEME API (data-fair)** | 15.4M de DPE, filter par commune/adresse | `https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines` | `https://data.ademe.fr/datasets/dpe03existant/api-doc` |
| **ADEME dump SQL** | Bulk PostgreSQL complet | `https://opendata.ademe.fr/dump_dpev2_prod_fdld.sql.gz` | `https://data.ademe.fr/datasets/dpe03existant` |

**Champs clés** : `etiquette_dpe` (A-G), `conso_5_usages_par_m2_ep`, `adresse_ban`, `code_postal_ban`, `_geopoint`, `surface_habitable_immeuble`

**Exemple** — DPE d'une adresse :
```
https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines?q=25+Rue+de+Belfort+Carcassonne&select=numero_dpe,adresse_ban,etiquette_dpe
```

⚠️ Pas de référence cadastrale dans les données DPE → join spatial via `_geopoint` + parcelle cadastre.

---

## 9. Loyers — Marché locatif

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **Carte des loyers** | Loyer €/m² par commune (ANIL) | `https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune` | `https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune` |
| **OLL** | Observatoires Locaux des Loyers | `https://www.data.gouv.fr/fr/organizations/observatoires-locaux-des-loyers/` | `https://www.data.gouv.fr/fr/organizations/observatoires-locaux-des-loyers/` |
| **Encadrement Paris** | Loyers encadrés par quartier | `https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/` | `https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/` |

---

## 10. Taxe foncière

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **REI (DGFiP)** | Bases, taux, produits par commune | `https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4` | `https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4` |
| **Fiscalité locale Géo** | Taux votés par commune (TFPB, TH, etc.) | `https://www.data.gouv.fr/datasets/fiscalite-locale-des-particuliers-geo` | `https://www.data.gouv.fr/datasets/fiscalite-locale-des-particuliers-geo` |
| **impots.gouv.fr stats** | Taux votés XLSX | `https://www.impots.gouv.fr/statistiques-collectivites-locales` | `https://www.impots.gouv.fr/statistiques-collectivites-locales` |

---

## 11. Risques industriels & technologiques

> Critères : proximité sites nucléaires (INB), sites SEVESO (seuil haut/bas), ICPE, sols pollués, anciennes mines/carrières, lignes haute tension. **Sources via API Géorisques V2** (voir §5) + ODRÉ.

| Risque | Source | URL / Endpoint | Api doc |
|---|---|---|---|
| **INB (nucléaire)** | Géorisques V2 | `/api/v2/installations_nucleaires?codesParcelle=...&rayon=...` | `https://www.georisques.gouv.fr/doc-api` |
| **SEVESO / ICPE** | Géorisques V2 | `/api/v2/installations_classees?statutSeveso=SEUIL_HAUT` | `https://www.georisques.gouv.fr/doc-api` |
| **Sols pollués (SIS/BASOL)** | Géorisques V2 | `/api/v2/ssp` (+ `/casias`, `/conclusions_sis`) | `https://www.georisques.gouv.fr/doc-api` |
| **Mines & carrières** | Géorisques V2 | `/api/v2/cavites` + `/api/v2/gaspar/pprm` | `https://www.georisques.gouv.fr/doc-api` |
| **Lignes HT (63-400 kV)** | ODRÉ (RTE) | `https://odre.opendatasoft.com/explore/dataset/lignes-aeriennes-rte-nv/` | `https://odre.opendatasoft.com/explore/dataset/lignes-aeriennes-rte-nv/` |
| **Lignes HT souterraines** | ODRÉ (RTE) | `https://odre.opendatasoft.com/explore/dataset/lignes-souterraines-rte-nv/` | `https://odre.opendatasoft.com/explore/dataset/lignes-souterraines-rte-nv/` |
| **Postes électriques** | ODRÉ (RTE) | `https://odre.opendatasoft.com/explore/dataset/postes-electriques-rte/` | `https://odre.opendatasoft.com/explore/dataset/postes-electriques-rte/` |
| **Lignes HTA (20 kV)** | Enedis | `https://opendata.enedis.fr/datasets/reseau-hta` | `https://opendata.enedis.fr/datasets/reseau-hta` |
| **ICPE bulk national** | Géorisques (bases de données) | `https://www.georisques.gouv.fr/donnees/bases-de-donnees` | `https://www.georisques.gouv.fr/donnees/bases-de-donnees` |

**Notes d'implémentation** :
- Géorisques V2 accepte `codesParcelle` + `rayon` → jointure directe parcelle → risques dans un rayon.
- Lignes HT = **polylignes** sur ODRÉ → distance spatiale PostGIS (`ST_Distance(parcelle, ligne)`), pas de join point-rayon.
- Licence Ouverte 2.0 partout ; V2 nécessite un token gratuit (Cerbère).

---

## 12. Climat actuel & projections futures

> Critères : normales climatiques (température, précipitations, ensoleillement), projections 2050/2100, canicule, sécheresse, gel, vent. Granularité max officielle : **commune** (ou grille SAFRAN 8 km) — pas de climat par parcelle.

### 12a. Climat actuel — normales 1991-2020

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **API Météo-France** | Normales, quotidiennes, mensuelles (compte gratuit + token, 50 req/min) | `https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie` | `https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie` |
| **Fiches climatologiques** | PDF + données par station (`tmin`, `tmax`, `rr`, `ensoleillement`) — **sans clé** | `https://www.data.gouv.fr/datasets/fiches-climatologiques` | `https://www.data.gouv.fr/datasets/fiches-climatologiques` |
| **Données quotidiennes bulk** | csv.gz par département, **sans clé** | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-quotidiennes` | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-quotidiennes` |
| **Données mensuelles bulk** | csv.gz | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-mensuelles` | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-mensuelles` |

**Granularité** : stations (~1000 temp., ~3500 pluviomètres) → join commune par station la plus proche ou interpolation.

### 12b. Projections futures — DRIAS-2020

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **DRIAS** | Euro-Cordex 8 km, quotidien 2006-2100, RCP2.6/4.5/8.5, 50+ indices (canicule, sols secs, risque feu, gel) avec quantiles multi-modèles | `https://www.drias-climat.fr/` (compte gratuit) | `https://drias-climat.fr/commande` |
| **Indicateurs TRACC** | 42 indicateurs par niveau de réchauffement (+2°C, +2.7°C, +4°C) | Via DRIAS | `https://drias-climat.fr/commande` |
| **Climadiag Commune** | Indicateurs par commune à 2030/2050/2100 : jours très chauds (>35°C), nuits chaudes, vagues de chaleur, sol sec, risque feu — **PDF par commune, pas d'API bulk** | `https://meteofrance.com/climadiag-commune` | `https://meteofrance.com/climadiag-commune` |

### 12c. Sécheresse / humidité des sols

| Source | Usage | URL | Api doc |
|---|---|---|---|
| **SIM quotidienne** | SWI (Soil Wetness Index 0-1, <0.5 = sol sec), grille 8 km | `https://www.data.gouv.fr/datasets/donnees-changement-climatique-sim-quotidienne` | `https://www.data.gouv.fr/datasets/donnees-changement-climatique-sim-quotidienne` |
| **VigiEau** | Restrictions sécheresse en vigueur (remplace Propluvia, décommissionné) | `https://vigieau.gouv.fr` | `https://api.vigieau.beta.gouv.fr/swagger` |

---

## 13. Risques climatiques émergents

| Risque | Source | URL | Api doc |
|---|---|---|---|
| **Feux de forêt** | Géorisques V1 `risques` (FEUFORET) + `old` | `https://georisques.gouv.fr/api/v1/` | `https://www.georisques.gouv.fr/doc-api` |
| **Historique feux** | BDIFF (IGN), par commune, 2006-2022 | `https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff` | `https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff` |
| **Submersion marine** | Géorisques V1 `azi` / `ppr` (PPRL) | `https://georisques.gouv.fr/api/v1/` | `https://www.georisques.gouv.fr/doc-api` |
| **Érosion côtière** | GéoLittoral (Cerema) — recul événementiel, indicateur national | `https://www.geolittoral.developpement-durable.gouv.fr/` | `https://www.geolittoral.developpement-durable.gouv.fr/telechargement-et-flux-de-donnees-a802.html` |
| **Communes RTC** | Liste légale (décret 2022-750 modifié 2026-95 : **371 communes**) — flag binaire | `https://www.data.gouv.fr/datasets/liste-des-communes-volontaires-pour-sadapter-au-recul-du-trait-de-cote` | `https://www.data.gouv.fr/datasets/liste-des-communes-volontaires-pour-sadapter-au-recul-du-trait-de-cote` |

**Score composite climat** : pas de score officiel unique. Modèle : note SDES « La vulnérabilité des communes aux risques climatiques » (`https://www.statistiques.developpement-durable.gouv.fr/`). Réf. tierce ouverte (non officielle) : ClimaScore (`https://climascore.fr/`, GitHub climScore).

---

## 14. Servitudes & protections du patrimoine

> Critères : servitudes d'utilité publique (SUP), monuments historiques + périmètres ABF, sites classés/inscrits, UNESCO, Natura 2000, ZNIEFF, zones humides, espaces boisés classés, SPR, plans d'exposition au bruit (PEB).

**⭐ Point d'accès unifié : Géoplateforme WFS** — `https://data.geopf.fr/wfs/ows?service=WFS&version=2.0.0&request=GetCapabilities` — couches vectorielles vérifiées :

| Couche WFS | Contenu |
|---|---|
| `wfs_sup:servitude` (+ `servitude_acte_sup`) | Servitudes d'utilité publique (assiettes surfaciques) |
| `patrinat_bpm` | Bien patrimoine mondial UNESCO |
| `patrinat_znieff1` / `znieff1_mer` | ZNIEFF type 1 |
| `patrinat_znieff2` / `znieff2_mer` | ZNIEFF type 2 |
| `patrinat_zps` / `patrinat_sic` | Natura 2000 (ZPS + SIC/ZSC) |
| `sites_metropole_gpkg_*:STE_Metropole` | Sites classés + inscrits (métropole) |
| `dgac_peb_arrete_wfs` | Plans d'exposition au bruit (aérodromes, zones A/B/C/D) |
| `TOURBIERES_ZONES-HUMIDES.BCAE:bcae` | Zones humides + tourbières BCAE 2025 |
| `ONF.FORETS_PUBLIQUES` | Forêts publiques ONF |

| Protection | Source | URL | Api doc |
|---|---|---|---|
| **Monuments historiques** | API Ministère de la Culture (base Mérimée, points, MAJ jeudi) | `https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/records` | `https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/` |
| **Périmètres ABF (500m/PPA/PPM)** | Atlas des patrimoines (polygones) | `http://atlas.patrimoines.culture.fr/` | `http://atlas.patrimoines.culture.fr/` |
| **Sites patrimoniaux remarquables (SPR)** | API Ministère de la Culture (940+, niveau commune) | `https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/liste-des-sites-patrimoniaux-remarquables-spr/records` | `https://data.culture.gouv.fr/explore/dataset/liste-des-sites-patrimoniaux-remarquables-spr/` |
| **Natura 2000 / ZNIEFF bulk** | data.gouv.fr (miroir INPN, MAJ quotidienne) | `https://www.data.gouv.fr/datasets/inpn-donnees-du-programme-natura-2000` + `...-znieff` | `https://www.data.gouv.fr/datasets/inpn-donnees-du-programme-natura-2000` |
| **Espaces boisés classés (EBC)** | Via GPU / API Carto (même pipeline que PLU) | `https://apicarto.ign.fr/api/gpu/zone-urba` | `https://apicarto.ign.fr/api/doc/gpu` |

**⚠️ Régimes de contrainte à distinguer dans le scoring** :
- **Durs** : EBC (défrichement rejeté de plein droit), forêts de protection, PEB zones A/B (construction interdite), sites classés, périmètres monuments (avis ABF).
- **Procéduraux / inventaires** : Natura 2000 (évaluation des incidences), ZNIEFF (inventaire, pas une protection), zones humides (autorisation/compensation L.211-1).
- SUP = couche de travail non exhaustive / non opposable → signal, pas vérité légale.
- ⚠️ INPN (inpn.mnhn.fr) temporairement down (cyberattaque MNHN) → utiliser les miroirs data.gouv.fr.

---

## 15. Réseaux & desserte

> Critères : fibre, électricité, gaz, eau potable, assainissement, couverture mobile, écoles, santé, bornes incendie.

| Desserte | Source | URL / Granularité | Api doc |
|---|---|---|---|
| **Fibre (THD)** | ARCEP « Ma connexion internet » — **par adresse/bâtiment** (`eligibilite`, `base_imb`) + stats par commune | `https://data.arcep.fr/fixe/maconnexioninternet/` | `https://data.arcep.fr/fixe/maconnexioninternet/` |
| **Couverture mobile** | ARCEP « Mon réseau mobile » — grille ~200 m + sites antennes | `https://data.arcep.fr/mobile/` | `https://data.arcep.fr/mobile/` |
| **Électricité (réseau)** | Enedis (lignes BT/HTA, postes — géolocalisées) | `https://opendata.enedis.fr/` | `https://opendata.enedis.fr/` |
| **Électricité (national)** | ODRÉ / Agence ORE (tous les opérateurs) | `https://opendata.reseaux-energies.fr/` | `https://opendata.reseaux-energies.fr/` |
| **Gaz (réseau)** | GRDF (canalisations, ~9513 communes, champ `insee_commune_admin`) | `https://opendata.grdf.fr/explore/dataset/cartographie-du-reseau-grdf-en-service/` | `https://opendata.grdf.fr/explore/dataset/cartographie-du-reseau-grdf-en-service/` |
| **Eau potable** | SISPEA / EauFrance (composition communale des services) | `https://www.services.eaufrance.fr/pro/telechargement` | `https://www.services.eaufrance.fr/pro/telechargement` |
| **Assainissement collectif / non collectif** | SISPEA (mêmes fichiers : AC + ANC/SPANC) | `https://www.services.eaufrance.fr/pro/telechargement` | `https://www.services.eaufrance.fr/pro/telechargement` |
| **Écoles** | Adresse et géolocalisation des établissements (1er/2nd degré) | `https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/` | `https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/` |
| **Santé (hôpitaux, EHPAD...)** | FINESS (Min. Santé) | `https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements/` | `https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements/` |
| **Bornes incendie** | Pas de source nationale officielle → OSM (`emergency=fire_hydrant`, ODbL) + schéma PEI | `https://schema.data.gouv.fr/datakode/schema-pei/latest.html` | `https://schema.data.gouv.fr/datakode/schema-pei/latest.html` |
| **Commerces / équipements** | INSEE BPE (commune/IRIS, officiel) + BANCO (adresse, ODbL) | `https://www.data.gouv.fr/datasets/base-permanente-des-equipements-1` + `...base-nationale-des-commerces-ouverte` | `https://www.data.gouv.fr/datasets/base-permanente-des-equipements-1` |

**Licences** : LO 2.0 pour tout sauf BANCO, poteaux Enedis, bornes OSM = **ODbL** (attribution si redistribution).

---

## 16. Nuisances & environnement

> Critères : qualité de l'air, bruit, ondes (antennes), lignes HT, pollution lumineuse, verdure, moustique tigre, ambroisie, termites.

| Nuisance | Source | URL / Granularité | Api doc |
|---|---|---|---|
| **Qualité de l'air (indice ATMO)** | Atmo Data (par commune, quotidien + prévision J+1) | `https://admindata.atmo-france.org/api/doc/v2` (ODbL, inscription gratuite) | `https://admindata.atmo-france.org/api/doc/v2` |
| **Concentrations PM2.5/PM10/NO2** | Geod'air (INERIS/LCSQA, par station) | `https://www.geodair.fr/donnees/api` | `https://www.geodair.fr/donnees/api` |
| **Bruit (routes/rails)** | Cartes de bruit stratégiques Cerema — zones Lden/Lnight, MAJ 5 ans | `https://www.data.gouv.fr/datasets/cartes-de-bruit-strategiques-des-reseaux-routiers-et-ferroviaires-non-concedes-directive-europeenne-2002-49-ce` | `https://www.data.gouv.fr/datasets/cartes-de-bruit-strategiques-des-reseaux-routiers-et-ferroviaires-non-concedes-directive-europeenne-2002-49-ce` |
| **Bruit (aéroports)** | PEB DGAC via Géoplateforme WFS (voir §14) | `dgac_peb_arrete_wfs` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/diffusion` |
| **Antennes relais** | ANFR (`data.anfr.fr`, API + GeoJSON) | `https://data.anfr.fr/api` | `https://data.anfr.fr/api` |
| **Pollution lumineuse** | ONB/SDES (grille 500 m, mag/arcsec²) | `https://www.notre-environnement.gouv.fr/indicateurs/proportion-du-territoire-hexagonal-fortement-impacte-par-la-pollution-lumineuse-en` | `https://www.notre-environnement.gouv.fr/indicateurs/proportion-du-territoire-hexagonal-fortement-impacte-par-la-pollution-lumineuse-en` |
| **Verdure (forêts, parcs)** | CORINE Land Cover (polygones 44 classes) ou OSM | `https://www.data.gouv.fr/datasets/corine-land-cover-occupation-des-sols-en-france/` | `https://www.data.gouv.fr/datasets/corine-land-cover-occupation-des-sols-en-france/` |
| **Moustique tigre** | ANSES — liste communes colonisées (pas d'API bulk) | `https://signalement-moustique.anses.fr/signalement_albopictus/colonisees` | `https://signalement-moustique.anses.fr/signalement_albopictus/colonisees` |
| **Ambroisie** | Observatoire des ambroisies (FREDON France), cartes annuelles | `https://ambroisie-risque.info/` | `https://ambroisie-risque.info/` |
| **Termites** | Carto nationale Cerema + arrêtés DDT par département | `https://www.cerema.fr/fr/actualites/cartographie-nationale-termites-merules` | `https://www.cerema.fr/fr/actualites/cartographie-nationale-termites-merules` |

**Radon** : déjà couvert par Géorisques V1 (`/api/v1/radon`, potentiel 1-3 par commune).

---

## Résumé rapide

| Besoin | Source principale | Endpoint |
|---|---|---|
| Parcelles | API Carto cadastre | `apicarto.ign.fr/api/cadastre/parcelle` |
| Transactions | Geo-DVF | `files.data.gouv.fr/geo-dvf/latest/csv/` |
| Prix m² | Statistiques DVF | `data.gouv.fr/datasets/statistiques-dvf` |
| Zones constructibles | API Carto GPU | `apicarto.ign.fr/api/gpu/zone-urba` |
| Pente / exposition | IGN Altimétrie | `data.geopf.fr/altimetrie/...` |
| Risques naturels | Géorisques V1/V2 | `georisques.gouv.fr/api/v1/` + `/api/v2/` |
| Nucléaire / SEVESO / ICPE | Géorisques V2 | `/api/v2/installations_nucleaires` + `/installations_classees` |
| Sols pollués | Géorisques V2 | `/api/v2/ssp` |
| Lignes HT | ODRÉ (RTE) | `odre.opendatasoft.com` |
| Climat actuel | Météo-France normales 1991-2020 | `data.gouv.fr/datasets/fiches-climatologiques` |
| Climat futur | DRIAS-2020 / Climadiag Commune | `drias-climat.fr` |
| Feux de forêt | Géorisques FEUFORET + BDIFF | `georisques.gouv.fr/api/v1/risques` |
| Submersion / érosion | Géorisques AZI/PPR + GéoLittoral | `geolittoral.developpement-durable.gouv.fr` |
| Servitudes / patrimoine | Géoplateforme WFS + data.culture.gouv.fr | `data.geopf.fr/wfs/ows` |
| Natura 2000 / ZNIEFF | Géoplateforme WFS | `patrinat_zps` / `patrinat_znieff1/2` |
| Fibre | ARCEP Ma connexion internet | `data.arcep.fr/fixe/maconnexioninternet/` |
| Mobile | ARCEP Mon réseau mobile | `data.arcep.fr/mobile/` |
| Élec / gaz | Enedis / GRDF / ODRÉ | `opendata.enedis.fr` / `opendata.grdf.fr` |
| Eau / assainissement | SISPEA | `services.eaufrance.fr/pro/telechargement` |
| Écoles / santé | data.education.gouv.fr / FINESS | `data.gouv.fr/...` |
| Qualité de l'air | Atmo Data | `admindata.atmo-france.org/api/doc/v2` |
| Bruit | Cartes de bruit Cerema | `data.gouv.fr/datasets/cartes-de-bruit-strategiques...` |
| Antennes | ANFR | `data.anfr.fr/api` |
| Transport / POI | IGN + OSM | `data.geopf.fr/geocodage` + Overpass |
| Eau souterraine | Hub'Eau | `hubeau.eaufrance.fr/api/v1/niveaux_nappes/` |
| DPE | ADEME | `data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/` |
| Loyers | Carte des loyers | `data.gouv.fr/datasets/carte-des-loyers` |
| Taxe foncière | REI DGFiP | `data.gouv.fr/datasets/...rei-4` |
