# Plot — Open Data Sources

All sources below are **free**, under **Licence Ouverte 2.0** (unless noted), with no API key required (unless explicitly stated).

---

## 1. Cadastre (parcels, boundaries, areas)

| Source | Usage | URL | API doc |
|---|---|---|---|
| **API Carto — Cadastre** | Parcel by ID, by zone, by geom | `https://apicarto.ign.fr/api/cadastre/parcelle` | `https://apicarto.ign.fr/api/doc/cadastre` |
| **Geoplateforme WFS** | Spatial queries (bbox, CQL) | `https://data.geopf.fr/wfs/ows` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/diffusion` |
| **Etalab bulk** | Full GeoJSON download by department | `https://cadastre.data.gouv.fr/data/etalab-cadastre/` | `https://cadastre.data.gouv.fr/` |

**Key fields returned**: `idu` (parcel ID, 14 chars), `contenance` (area m²), `geometry` (MultiPolygon WGS84), `code_insee`, `section`, `numero`

**Example**:
```
https://apicarto.ign.fr/api/cadastre/parcelle?code_insee=44109&section=EX&numero=0080
```

---

## 2. DVF — Property Transactions

| Source | Usage | URL | API doc |
|---|---|---|---|
| **Geo-DVF** | Geolocalized transactions by year/department | `https://files.data.gouv.fr/geo-dvf/latest/csv/{YEAR}/{DEPT}.csv.gz` | `https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/` |
| **DVF Statistics** | Average/median price per sqm by commune | `https://www.data.gouv.fr/datasets/statistiques-dvf` | `https://www.data.gouv.fr/datasets/statistiques-dvf` |
| **VALORIS API** | REST — median price by commune | `https://www.valoris-immo.fr/api/v1/prix-median` | `https://www.valoris-immo.fr/api/v1/docs` |
| **DVF+ (Cerema)** | Enriched data, geomutations | `https://www.data.gouv.fr/datasets/dvf-open-data` | `https://www.data.gouv.fr/datasets/dvf-open-data` |

**Geo-DVF example**:
```
https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departments/75.csv.gz
```

⚠️ DVF excludes Alsace-Moselle and Mayotte.

---

## 3. PLU / PLUi — Buildable Zones

| Source | Usage | URL | API doc |
|---|---|---|---|
| **API Carto — GPU** | Urban zone by geometry | `https://apicarto.ign.fr/api/gpu/zone-urba` | `https://apicarto.ign.fr/api/doc/gpu` |
| **GPU API** | PLU documents, regulation downloads | `https://www.geoportail-urbanisme.gouv.fr/api/` | `https://www.geoportail-urbanisme.gouv.fr/api/` |
| **Zones PLU France** | National full GeoParquet | `https://www.data.gouv.fr/datasets/zones-plu-france` | `https://www.data.gouv.fr/datasets/zones-plu-france` |

**Key fields**: `libelle` (Uc, etc.), `destdomi` (purpose), `urlfic` (regulation PDF)

**Example**:
```
https://apicarto.ign.fr/api/gpu/zone-urba?geom={"type":"Point","coordinates":[2.35,48.85]}&insee=75056
```

---

## 4. Altimetry / DEM (slope, aspect)

| Source | Usage | URL | API doc |
|---|---|---|---|
| **IGN Altimetry REST** | Elevation of a point or profile | `https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/altimetrie` |
| **RGE ALTI®** | DEM 1m/5m (download or WMTS) | `https://cartes.gouv.fr/catalogue/dataset/IGNF_RGE-ALTI` | `https://geoservices.ign.fr/documentation/donnees/alti/rgealti` |
| **LiDAR HD** | High-resolution DEM 1m | Via cartes.gouv.fr | `https://geoservices.ign.fr/lidarhd` |

**Example** — point elevation:
```
https://data.geopf.fr/altimetrie/1.0/calcul/alti/rest/elevation.json?lon=2.35&lat=48.85&resource=ign_rge_alti_wld
```

**Slope/aspect calculation**: sample a grid of points around the parcel, compute the gradient locally.

---

## 5. Natural Risks (Georisques / BRGM)

| Source | Usage | URL | API doc |
|---|---|---|---|
| **Georisques API** | Clay, radon, flooding, earthquake, PPR | `https://georisques.gouv.fr/api/v1/` | `https://www.georisques.gouv.fr/doc-api` |

**V1 Endpoints**:
| Risk | Endpoint |
|---|---|
| Clay (shrink-swell) | `/api/v1/argiles` |
| Radon | `/api/v1/radon` |
| Flooding (AZI) | `/api/v1/azi` |
| PPR | `/api/v1/ppr` |
| Underground cavities | `/api/v1/cavites` |
| Ground movement | `/api/v1/mvt` |
| Seismicity | `/api/v1/zonage_sismique` |
| Historical NATCAT | `/api/v1/catnat` |
| Forest fires (zoning) | `/api/v1/risques` (risk `FEUFORET`) |
| OLD (clearance obligations) | `/api/v1/old` |
| Full report (JSON) | `/api/v1/resultats_rapport_risque` |

**Example**:
```
https://georisques.gouv.fr/api/v1/argiles?code_insee=75056
```

### Georisques API V2 — by cadastral parcel ⭐

The **V2 API** (doc: `https://www.georisques.gouv.fr/doc-api`) accepts `codesParcelle` + `rayon` (meters), `geometry` (WKT), `longitude`/`latitude`, `codesInsee` — the ideal query mode for parcel-level scoring. Free token (Cerbere/FranceConnect, valid 1 year) sent in header `X-API-Key`. Rate limit: 1000 req/min/IP.

| Endpoint | Content |
|---|---|
| `/api/v2/installations_nucleaires` | Basic nuclear installations (INB) |
| `/api/v2/installations_classees` | ICPE + `statutSeveso` filter (SEUIL_HAUT/SEUIL_BAS) |
| `/api/v2/ssp` | Contaminated sites (SIS/BASOL) + `/casias` + `/conclusions_sis` |
| `/api/v2/cavites` | Underground cavities (quarries, caves, marl pits) |
| `/api/v2/gaspar/pprm` | Mining Risk Prevention Plans |

---

## 6. Transport / POI / Geocoding

| Source | Usage | URL | API doc |
|---|---|---|---|
| **IGN Geocoding** | Address → coordinates | `https://data.geopf.fr/geocodage/search` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage` |
| **IGN Reverse Geocoding** | Coordinates → address | `https://data.geopf.fr/geocodage/reverse` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/geocodage` |
| **IGN Routing** | Distance/travel time | `https://data.geopf.fr/navigation/itineraire` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/itineraire` |
| **IGN Isochrone** | Accessibility zones | `https://data.geopf.fr/navigation/isochrone` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/isochrone` |
| **Overpass API** | OSM POIs (schools, shops, transit) | `https://overpass-api.de/api/interpreter` | `https://wiki.openstreetmap.org/wiki/Overpass_API` |

---

## 7. Groundwater (Water Table)

| Source | Usage | URL | API doc |
|---|---|---|---|
| **Hub'Eau Piezometry** | Piezometric stations, water table levels | `https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/` | `https://hubeau.eaufrance.fr/page/api-piezometrie` |

**Endpoints**:
- `/stations` — station list
- `/chroniques` — time series (water table level)
- `/chroniques_tr` — real-time data (~1500 sensors)

**Example**:
```
https://hubeau.eaufrance.fr/api/v1/niveaux_nappes/stations?code_commune=62193&format=json
```

---

## 8. DPE — Energy Performance Diagnosis

| Source | Usage | URL | API doc |
|---|---|---|---|
| **ADEME API (data-fair)** | 15.4M DPE records, filter by commune/address | `https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines` | `https://data.ademe.fr/datasets/dpe03existant/api-doc` |
| **ADEME SQL dump** | Full bulk PostgreSQL | `https://opendata.ademe.fr/dump_dpev2_prod_fdld.sql.gz` | `https://data.ademe.fr/datasets/dpe03existant` |

**Key fields**: `etiquette_dpe` (A-G), `conso_5_usages_par_m2_ep`, `adresse_ban`, `code_postal_ban`, `_geopoint`, `surface_habitable_immeuble`

**Example** — DPE for an address:
```
https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines?q=25+Rue+de+Belfort+Carcassonne&select=numero_dpe,adresse_ban,etiquette_dpe
```

⚠️ No cadastral reference in DPE data → spatial join via `_geopoint` + cadastre parcel.

---

## 9. Rent — Rental Market

| Source | Usage | URL | API doc |
|---|---|---|---|
| **Carte des loyers** | Rent €/sqm by commune (ANIL) | `https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune` | `https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune` |
| **OLL** | Local Rent Observatories | `https://www.data.gouv.fr/fr/organizations/observatoires-locaux-des-loyers/` | `https://www.data.gouv.fr/fr/organizations/observatoires-locaux-des-loyers/` |
| **Encadrement Paris** | Rent-controlled rates by neighborhood | `https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/` | `https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/` |

---

## 10. Property Tax

| Source | Usage | URL | API doc |
|---|---|---|---|
| **REI (DGFiP)** | Tax bases, rates, revenue by commune | `https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4` | `https://www.data.gouv.fr/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-directe-locale-rei-4` |
| **Fiscalite locale Geo** | Voted rates by commune (TFPB, TH, etc.) | `https://www.data.gouv.fr/datasets/fiscalite-locale-des-particuliers-geo` | `https://www.data.gouv.fr/datasets/fiscalite-locale-des-particuliers-geo` |
| **impots.gouv.fr stats** | Voted rates XLSX | `https://www.impots.gouv.fr/statistiques-collectivites-locales` | `https://www.impots.gouv.fr/statistiques-collectivites-locales` |

---

## 11. Industrial & Technological Risks

> Criteria: proximity to nuclear sites (INB), SEVESO sites (high/low threshold), ICPE, contaminated sites, former mines/quarries, high-voltage lines. **Sources via Georisques API V2** (see §5) + ODRE.

| Risk | Source | URL / Endpoint | API doc |
|---|---|---|---|
| **INB (nuclear)** | Georisques V2 | `/api/v2/installations_nucleaires?codesParcelle=...&rayon=...` | `https://www.georisques.gouv.fr/doc-api` |
| **SEVESO / ICPE** | Georisques V2 | `/api/v2/installations_classees?statutSeveso=SEUIL_HAUT` | `https://www.georisques.gouv.fr/doc-api` |
| **Contaminated sites (SIS/BASOL)** | Georisques V2 | `/api/v2/ssp` (+ `/casias`, `/conclusions_sis`) | `https://www.georisques.gouv.fr/doc-api` |
| **Mines & quarries** | Georisques V2 | `/api/v2/cavites` + `/api/v2/gaspar/pprm` | `https://www.georisques.gouv.fr/doc-api` |
| **HV lines (63-400 kV)** | ODRE (RTE) | `https://odre.opendatasoft.com/explore/dataset/lignes-aeriennes-rte-nv/` | `https://odre.opendatasoft.com/explore/dataset/lignes-aeriennes-rte-nv/` |
| **Underground HV lines** | ODRE (RTE) | `https://odre.opendatasoft.com/explore/dataset/lignes-souterraines-rte-nv/` | `https://odre.opendatasoft.com/explore/dataset/lignes-souterraines-rte-nv/` |
| **Substations** | ODRE (RTE) | `https://odre.opendatasoft.com/explore/dataset/postes-electriques-rte/` | `https://odre.opendatasoft.com/explore/dataset/postes-electriques-rte/` |
| **HTA lines (20 kV)** | Enedis | `https://opendata.enedis.fr/datasets/reseau-hta` | `https://opendata.enedis.fr/datasets/reseau-hta` |
| **ICPE national bulk** | Georisques (databases) | `https://www.georisques.gouv.fr/donnees/bases-de-donnees` | `https://www.georisques.gouv.fr/donnees/bases-de-donnees` |

**Implementation notes**:
- Georisques V2 accepts `codesParcelle` + `rayon` → direct parcel join → risks within radius.
- HV lines = **polylines** on ODRE → PostGIS spatial distance (`ST_Distance(parcel, line)`), no point-radius join.
- Licence Ouverte 2.0 everywhere; V2 requires a free token (Cerbere).

---

## 12. Current Climate & Future Projections

> Criteria: climate normals (temperature, precipitation, sunshine), 2050/2100 projections, heat waves, drought, frost, wind. Max official granularity: **commune** (or SAFRAN 8 km grid) — no per-parcel climate.

### 12a. Current Climate — 1991-2020 Normals

| Source | Usage | URL | API doc |
|---|---|---|---|
| **Meteo-France API** | Normals, daily, monthly (free account + token, 50 req/min) | `https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie` | `https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesClimatologie` |
| **Climatological sheets** | PDF + data by station (`tmin`, `tmax`, `rr`, `sunshine`) — **no key** | `https://www.data.gouv.fr/datasets/fiches-climatologiques` | `https://www.data.gouv.fr/datasets/fiches-climatologiques` |
| **Daily bulk data** | csv.gz by department, **no key** | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-quotidiennes` | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-quotidiennes` |
| **Monthly bulk data** | csv.gz | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-mensuelles` | `https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-mensuelles` |

**Granularity**: stations (~1000 temp., ~3500 rain gauges) → join commune by nearest station or interpolation.

### 12b. Future Projections — DRIAS-2020

| Source | Usage | URL | API doc |
|---|---|---|---|
| **DRIAS** | Euro-Cordex 8 km, daily 2006-2100, RCP2.6/4.5/8.5, 50+ indices (heat wave, dry soils, fire risk, frost) with multi-model quantiles | `https://www.drias-climat.fr/` (free account) | `https://drias-climat.fr/commande` |
| **TRACC Indicators** | 42 indicators by warming level (+2°C, +2.7°C, +4°C) | Via DRIAS | `https://drias-climat.fr/commande` |
| **Climadiag Commune** | Per-commune indicators for 2030/2050/2100: very hot days (>35°C), warm nights, heat waves, dry soil, fire risk — **PDF per commune, no bulk API** | `https://meteofrance.com/climadiag-commune` | `https://meteofrance.com/climadiag-commune` |

### 12c. Drought / Soil Moisture

| Source | Usage | URL | API doc |
|---|---|---|---|
| **SIM daily** | SWI (Soil Wetness Index 0-1, <0.5 = dry soil), 8 km grid | `https://www.data.gouv.fr/datasets/donnees-changement-climatique-sim-quotidienne` | `https://www.data.gouv.fr/datasets/donnees-changement-climatique-sim-quotidienne` |
| **VigiEau** | Active drought restrictions (replaces Propluvia, decommissioned) | `https://vigieau.gouv.fr` | `https://api.vigieau.beta.gouv.fr/swagger` |

---

## 13. Emerging Climate Risks

| Risk | Source | URL | API doc |
|---|---|---|---|
| **Forest fires** | Georisques V1 `risques` (FEUFORET) + `old` | `https://georisques.gouv.fr/api/v1/` | `https://www.georisques.gouv.fr/doc-api` |
| **Fire history** | BDIFF (IGN), by commune, 2006-2022 | `https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff` | `https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff` |
| **Marine submersion** | Georisques V1 `azi` / `ppr` (PPRL) | `https://georisques.gouv.fr/api/v1/` | `https://www.georisques.gouv.fr/doc-api` |
| **Coastal erosion** | GeoLittoral (Cerema) — event-based retreat, national indicator | `https://www.geolittoral.developpement-durable.gouv.fr/` | `https://www.geolittoral.developpement-durable.gouv.fr/telechargement-et-flux-de-donnees-a802.html` |
| **RTC Communes** | Legal list (decree 2022-750 amended 2026-95: **371 communes**) — binary flag | `https://www.data.gouv.fr/datasets/liste-des-communes-volontaires-pour-sadapter-au-recul-du-trait-de-cote` | `https://www.data.gouv.fr/datasets/liste-des-communes-volontaires-pour-sadapter-au-recul-du-trait-de-cote` |

**Composite climate score**: no single official score. Model: SDES score "Commune vulnerability to climate risks" (`https://www.statistiques.developpement-durable.gouv.fr/`). Open third-party reference (unofficial): ClimaScore (`https://climascore.fr/`, GitHub climScore).

---

## 14. Easements & Heritage Protection

> Criteria: public utility easements (SUP), historic monuments + ABF perimeters, classified/registered sites, UNESCO, Natura 2000, ZNIEFF, wetlands, classified wooded areas (EBC), SPR, noise exposure plans (PEB).

**⭐ Unified access point: Geoplateforme WFS** — `https://data.geopf.fr/wfs/ows?service=WFS&version=2.0.0&request=GetCapabilities` — verified vector layers:

| WFS Layer | Content |
|---|---|
| `wfs_sup:servitude` (+ `servitude_acte_sup`) | Public utility easements (area-based) |
| `patrinat_bpm` | UNESCO World Heritage property |
| `patrinat_znieff1` / `znieff1_mer` | ZNIEFF type 1 |
| `patrinat_znieff2` / `znieff2_mer` | ZNIEFF type 2 |
| `patrinat_zps` / `patrinat_sic` | Natura 2000 (ZPS + SIC/SCI) |
| `sites_metropole_gpkg_*:STE_Metropole` | Classified + registered sites (mainland) |
| `dgac_peb_arrete_wfs` | Noise exposure plans (airports, zones A/B/C/D) |
| `TOURBIERES_ZONES-HUMIDES.BCAE:bcae` | Wetlands + peatlands BCAE 2025 |
| `ONF.FORETS_PUBLIQUES` | ONF public forests |

| Protection | Source | URL | API doc |
|---|---|---|---|
| **Historic monuments** | Ministry of Culture API (Merimee database, points, updated Thursday) | `https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/records` | `https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/` |
| **ABF perimeters (500m/PPA/PPM)** | Heritage atlas (polygons) | `http://atlas.patrimoines.culture.fr/` | `http://atlas.patrimoines.culture.fr/` |
| **Notable heritage sites (SPR)** | Ministry of Culture API (940+, commune level) | `https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/liste-des-sites-patrimoniaux-remarquables-spr/records` | `https://data.culture.gouv.fr/explore/dataset/liste-des-sites-patrimoniaux-remarquables-spr/` |
| **Natura 2000 / ZNIEFF bulk** | data.gouv.fr (INPN mirror, daily update) | `https://www.data.gouv.fr/datasets/inpn-donnees-du-programme-natura-2000` + `...-znieff` | `https://www.data.gouv.fr/datasets/inpn-donnees-du-programme-natura-2000` |
| **Classified wooded areas (EBC)** | Via GPU / API Carto (same pipeline as PLU) | `https://apicarto.ign.fr/api/gpu/zone-urba` | `https://apicarto.ign.fr/api/doc/gpu` |

**⚠️ Constraint regimes to distinguish in scoring**:
- **Hard**: EBC (clearing rejected by operation of law), protection forests, PEB zones A/B (construction prohibited), classified sites, monument perimeters (ABF opinion).
- **Procedural / inventories**: Natura 2000 (impact assessment), ZNIEFF (inventory, not a protection), wetlands (authorization/compensation L.211-1).
- SUP = working layer, non-exhaustive / non-opposable → signal, not legal truth.
- ⚠️ INPN (inpn.mnhn.fr) temporarily down (MNHN cyberattack) → use data.gouv.fr mirrors.

---

## 15. Networks & Services

> Criteria: fiber, electricity, gas, drinking water, sanitation, mobile coverage, schools, healthcare, fire hydrants.

| Service | Source | URL / Granularity | API doc |
|---|---|---|---|
| **Fiber (THD)** | ARCEP "Ma connexion internet" — **per address/building** (`eligibilite`, `base_imb`) + stats by commune | `https://data.arcep.fr/fixe/maconnexioninternet/` | `https://data.arcep.fr/fixe/maconnexioninternet/` |
| **Mobile coverage** | ARCEP "Mon reseau mobile" — ~200 m grid + antenna sites | `https://data.arcep.fr/mobile/` | `https://data.arcep.fr/mobile/` |
| **Electricity (network)** | Enedis (BT/HTA lines, substations — geolocated) | `https://opendata.enedis.fr/` | `https://opendata.enedis.fr/` |
| **Electricity (national)** | ODRE / ORE Agency (all operators) | `https://opendata.reseaux-energies.fr/` | `https://opendata.reseaux-energies.fr/` |
| **Gas (network)** | GRDF (pipelines, ~9513 communes, field `insee_commune_admin`) | `https://opendata.grdf.fr/explore/dataset/cartographie-du-reseau-grdf-en-service/` | `https://opendata.grdf.fr/explore/dataset/cartographie-du-reseau-grdf-en-service/` |
| **Drinking water** | SISPEA / EauFrance (municipal service composition) | `https://www.services.eaufrance.fr/pro/telechargement` | `https://www.services.eaufrance.fr/pro/telechargement` |
| **Collective / non-collective sanitation** | SISPEA (same files: AC + ANC/SPANC) | `https://www.services.eaufrance.fr/pro/telechargement` | `https://www.services.eaufrance.fr/pro/telechargement` |
| **Schools** | Address and geolocation of establishments (primary/secondary) | `https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/` | `https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/` |
| **Healthcare (hospitals, EHPAD...)** | FINESS (Min. Health) | `https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements/` | `https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements/` |
| **Fire hydrants** | No official national source → OSM (`emergency=fire_hydrant`, ODbL) + PEI schema | `https://schema.data.gouv.fr/datakode/schema-pei/latest.html` | `https://schema.data.gouv.fr/datakode/schema-pei/latest.html` |
| **Shops / amenities** | INSEE BPE (commune/IRIS, official) + BANCO (address, ODbL) | `https://www.data.gouv.fr/datasets/base-permanente-des-equipements-1` + `...base-nationale-des-commerces-ouverte` | `https://www.data.gouv.fr/datasets/base-permanente-des-equipements-1` |

**Licences**: LO 2.0 for everything except BANCO, Enedis poles, OSM hydrants = **ODbL** (attribution required on redistribution).

---

## 16. Nuisances & Environment

> Criteria: air quality, noise, RF (antennas), HV lines, light pollution, greenery, tiger mosquito, ragweed, termites.

| Nuisance | Source | URL / Granularity | API doc |
|---|---|---|---|
| **Air quality (ATMO index)** | Atmo Data (by commune, daily + J+1 forecast) | `https://admindata.atmo-france.org/api/doc/v2` (ODbL, free registration) | `https://admindata.atmo-france.org/api/doc/v2` |
| **PM2.5/PM10/NO2 concentrations** | Geod'air (INERIS/LCSQA, by station) | `https://www.geodair.fr/donnees/api` | `https://www.geodair.fr/donnees/api` |
| **Noise (roads/rail)** | Cerema strategic noise maps — Lden/Lnight zones, 5-year update | `https://www.data.gouv.fr/datasets/cartes-de-bruit-strategiques-des-reseaux-routiers-et-ferroviaires-non-concedes-directive-europeenne-2002-49-ce` | `https://www.data.gouv.fr/datasets/cartes-de-bruit-strategiques-des-reseaux-routiers-et-ferroviaires-non-concedes-directive-europeenne-2002-49-ce` |
| **Noise (airports)** | PEB DGAC via Geoplateforme WFS (see §14) | `dgac_peb_arrete_wfs` | `https://geoservices.ign.fr/documentation/services/services-geoplateforme/diffusion` |
| **Cell towers** | ANFR (`data.anfr.fr`, API + GeoJSON) | `https://data.anfr.fr/api` | `https://data.anfr.fr/api` |
| **Light pollution** | ONB/SDES (500 m grid, mag/arcsec²) | `https://www.notre-environnement.gouv.fr/indicateurs/proportion-du-territoire-hexagonal-fortement-impacte-par-la-pollution-lumineuse-en` | `https://www.notre-environnement.gouv.fr/indicateurs/proportion-du-territoire-hexagonal-fortement-impacte-par-la-pollution-lumineuse-en` |
| **Greenery (forests, parks)** | CORINE Land Cover (44-class polygons) or OSM | `https://www.data.gouv.fr/datasets/corine-land-cover-occupation-des-sols-en-france/` | `https://www.data.gouv.fr/datasets/corine-land-cover-occupation-des-sols-en-france/` |
| **Tiger mosquito** | ANSES — colonized commune list (no bulk API) | `https://signalement-moustique.anses.fr/signalement_albopictus/colonisees` | `https://signalement-moustique.anses.fr/signalement_albopictus/colonisees` |
| **Ragweed** | Ragweed Observatory (FREDON France), annual maps | `https://ambroisie-risque.info/` | `https://ambroisie-risque.info/` |
| **Termites** | National Cerema map + DDT prefectural orders by department | `https://www.cerema.fr/fr/actualites/cartographie-nationale-termites-merules` | `https://www.cerema.fr/fr/actualites/cartographie-nationale-termites-merules` |

**Radon**: already covered by Georisques V1 (`/api/v1/radon`, potential 1-3 per commune).

---

## Quick Reference

| Need | Primary Source | Endpoint |
|---|---|---|
| Parcels | API Carto cadastre | `apicarto.ign.fr/api/cadastre/parcelle` |
| Transactions | Geo-DVF | `files.data.gouv.fr/geo-dvf/latest/csv/` |
| Price/sqm | DVF Statistics | `data.gouv.fr/datasets/statistiques-dvf` |
| Buildable zones | API Carto GPU | `apicarto.ign.fr/api/gpu/zone-urba` |
| Slope / aspect | IGN Altimetry | `data.geopf.fr/altimetrie/...` |
| Natural risks | Georisques V1/V2 | `georisques.gouv.fr/api/v1/` + `/api/v2/` |
| Nuclear / SEVESO / ICPE | Georisques V2 | `/api/v2/installations_nucleaires` + `/installations_classees` |
| Contaminated sites | Georisques V2 | `/api/v2/ssp` |
| HV lines | ODRE (RTE) | `odre.opendatasoft.com` |
| Current climate | Météo-France normals 1991-2020 | `data.gouv.fr/datasets/fiches-climatologiques` |
| Future climate | DRIAS-2020 / Climadiag Commune | `drias-climat.fr` |
| Forest fires | Georisques FEUFORET + BDIFF | `georisques.gouv.fr/api/v1/risques` |
| Submersion / erosion | Georisques AZI/PPR + GeoLittoral | `geolittoral.developpement-durable.gouv.fr` |
| Easements / heritage | Geoplateforme WFS + data.culture.gouv.fr | `data.geopf.fr/wfs/ows` |
| Natura 2000 / ZNIEFF | Geoplateforme WFS | `patrinat_zps` / `patrinat_znieff1/2` |
| Fiber | ARCEP Ma connexion internet | `data.arcep.fr/fixe/maconnexioninternet/` |
| Mobile | ARCEP Mon reseau mobile | `data.arcep.fr/mobile/` |
| Electricity / gas | Enedis / GRDF / ODRE | `opendata.enedis.fr` / `opendata.grdf.fr` |
| Water / sanitation | SISPEA | `services.eaufrance.fr/pro/telechargement` |
| Schools / healthcare | data.education.gouv.fr / FINESS | `data.gouv.fr/...` |
| Air quality | Atmo Data | `admindata.atmo-france.org/api/doc/v2` |
| Noise | Cerema noise maps | `data.gouv.fr/datasets/cartes-de-bruit-strategiques...` |
| Antennas | ANFR | `data.anfr.fr/api` |
| Transport / POI | IGN + OSM | `data.geopf.fr/geocodage` + Overpass |
| Groundwater | Hub'Eau | `hubeau.eaufrance.fr/api/v1/niveaux_nappes/` |
| DPE | ADEME | `data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/` |
| Rent | Carte des loyers | `data.gouv.fr/datasets/carte-des-loyers` |
| Property tax | REI DGFiP | `data.gouv.fr/datasets/...rei-4` |
