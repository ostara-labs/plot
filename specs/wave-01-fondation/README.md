# Wave 01 — Fondation

> Fondations du produit : vision, stack technique, concepts clés, sources de données, modèle de données et architectures backend/frontend.

> Retour au [spec principal](../README.md)

---

## 1. Vision

Plot est un outil web qui aide les particuliers à trouver le meilleur logement en France, que ce soit pour y vivre ou pour investir. L'app combine données géospatiales, scoring intelligent et interface carte interactive. Les utilisateurs créent des "projets" de recherche qu'ils peuvent suivre dans le temps.

---

## 2. Stack

| Couche | Technologie |
|---|---|
| Frontend | SvelteKit + Skeleton Svelte + MapLibre GL JS |
| Backend | Python 3.12+ / FastAPI |
| Auth | FastAPI Users (open-source) |
| Données géo | geopandas, shapely, pyproj |
| Base de données | PostgreSQL + PostGIS |
| Tile server | Martin (vector tiles PostGIS → MapLibre) |
| Cache / Rate limit | Redis |
| Ingestion ETL | Airflow + dbt |
| Emails | Postmark (transactionnel + digest) |
| SMS | SMSemode / Sarbacane (OTP, alertes) |
| Analytics | Plausible |
| Monitoring | Sentry + Uptime Kuma |
| i18n | Paraglide (SvelteKit) — FR/EN |
| Déploiement | Docker Compose (dev) → Railway / ECS Fargate (prod) |

---

## 3. Internationalisation (i18n)

### Langues supportées

| Langue | Statut |
|---|---|
| 🇫🇷 Français | Langue par défaut |
| 🇬🇧 Anglais | Supporté dès le départ |
| 🗣️ Langues régionales | Wave future (breton, occitan, basque, corse, alsacien, etc.) |

### Stratégie

- **Frontend** : Paraglide (compilé, zero-runtime, basé sur MESSAGEFORMAT)
- **Backend** : Toutes les réponses API en JSON, le frontend gère la traduction
- **URL** : `/fr/...` et `/en/...` (routing par locale)
- **Détection** : Accept-Language header → cookie → défaut FR

### Structure des fichiers de traduction

```
frontend/
├── src/
│   ├── lib/
│   │   └── i18n/
│   │       ├── fr.json          # Référentiel (source de vérité)
│   │       ├── fr.meta.json     # Contexte et notes pour traducteurs
│   │       ├── en.json          # Traductions EN
│   │       └── index.ts         # Configuration i18n
```

### Référentiel FR (source de vérité)

Le français est la langue source. Chaque clé de traduction dispose d'un **fichier meta** contenant le contexte nécessaire à une traduction correcte.

**Format `fr.meta.json` :**

```json
{
  "project.new_button": {
    "context": "Bouton principal pour créer un nouveau projet de recherche",
    "usage": "Bouton sur la page d'accueil, toujours visible",
    "example": "L'utilisateur clique pour lancer le wizard de création",
    "notes": "Verbe d'action, doit être court et clair"
  },
  "filter.min_surface": {
    "context": "Label du slider de surface minimum en mètres carrés",
    "usage": "Panel de filtres latéral sur la carte",
    "example": "Surface min. : 500 m²",
    "notes": "Abréviation acceptée. Unité toujours en m²."
  },
  "annonce.statut.sous_offre": {
    "context": "Badge indiquant qu'un bien est en cours de vente (offre acceptée)",
    "usage": "Affiché sur les cards et fiches détaillées",
    "example": "Un autre acheteur a fait une offre acceptée",
    "notes": "Ne pas confondre avec 'vendu'. C'est un état transitoire."
  }
}
```

**Champs du meta :**

| Champ | Obligatoire | Description |
|---|---|---|
| `context` | ✅ | Sens de la phrase/clé dans l'application |
| `usage` | ✅ | Où et comment elle est affichée |
| `example` | ❌ | Exemple concret d'utilisation |
| `notes` | ❌ | Nuances, pièges à éviter, contraintes de traduction |

**Pourquoi un fichier séparé ?**
- Le `fr.json` reste propre et compilable (Paraglide le lit directement)
- Le `fr.meta.json` est un outil humain (traducteurs, réviseurs)
- Pas de surcharge dans le fichier de production
- Facile à extraire vers un outil de traduction (Crowdin, Lokalise, etc.)

### Contenu traduit

| Élément | Traduit ? |
|---|---|
| Interface (boutons, labels, navigation) | ✅ |
| Messages d'erreur | ✅ |
| Textes de contenu (descriptions biens) | ❌ (gardé dans la langue d'origine) |
| Noms de communes | ❌ (gardé tel quel) |
| Noms de rue | ❌ (gardé tel quel) |

### Règles

1. **Clés de traduction** : toujours en anglais, snake_case : `project.new_button`, `filter.min_surface`
2. **Falls back** : si une clé manque en EN, fallback sur FR
3. **Pluralisation** : gérée par Paraglide (match clé, one/other)
4. **Dates** : formatées selon la locale (Intl.DateTimeFormat)
5. **Nombres** : formatés selon la locale (1 234,56 en FR vs 1,234.56 en EN)

---

## 4. Concepts clés

### Le Projet

Un **projet** est une recherche sauvegardée avec ses critères. L'utilisateur crée un projet, le paramètre, et revient le consulter quand il veut. Le projet garde en mémoire la dernière recherche et affiche un indicateur de nouvelles offres depuis la dernière consultation.

### L'Annonce

Une **annonce** est la fiche d'un bien (terrain, maison, app) mise en ligne sur la plateforme. Elle peut être créée par un particulier, une agence ou un notaire. Chaque annonce a un statut et un propriétaire (celui qui l'a créée).

### Statut de l'annonce

| Statut | Description |
|---|---|
| **active** | Visible sur la plateforme |
| **sous_offre** | L'annonceur a indiqué que le bien est sous offre |
| **vendu** | Le bien a été vendu |
| **loué** | Le bien a été loué |
| **désactivée** | L'annonceur a désactivé temporairement |
| **supprimée** | L'annonceur a supprimé l'annonce |
| **signalée** | Signalée par un utilisateur comme indisponible |

### Droits selon le statut d'authentification

| Action | Déconnecté | Connecté (particulier) | Annonceur (pro/perso) |
|---|---|---|---|
| Rechercher / explorer la carte | ✅ | ✅ | ✅ |
| Créer un projet (local) | ✅ | — | — |
| Créer un projet (serveur) | ❌ | ✅ | ✅ |
| Être notifié de nouvelles offres | ❌ | ✅ | ✅ |
| Déposer une annonce | ❌ | ✅ | ✅ |
| Gérer ses annonces (supprimer, désactiver) | ❌ | — | ✅ |
| Récupérer un bien existant (prouver ownership) | ❌ | — | ✅ |
| **Signaler un bien indisponible** | **✅** | **✅** | **✅** |
| Contacter un vendeur | ❌ | ✅ | ✅ |

**Utilisateur déconnecté** : peut explorer la carte, créer des recherches locales (stockées dans le navigateur), et **signaler une annonce** (filtrage local + synchronisation si connexion ultérieure). Une alerte lui propose de créer un compte pour sauvegarder ses préférences.

---

## 12. Sources de données

Voir `docs/SOURCES.md` pour la liste complète.

Résumé :

| Source | Usage |
|---|---|
| API Carto Cadastre | Parcelles, limites, surfaces |
| Geo-DVF | Transactions immobilières |
| Statistiques DVF | Prix m² par commune |
| API Carto GPU | Zones constructibles PLU + EBC |
| IGN Altimétrie | Pente, exposition |
| Géorisques V1/V2 | Risques naturels, nucléaire, SEVESO, ICPE, sols pollués, mines (par parcelle + rayon via V2) |
| ODRÉ (RTE) / Enedis | Lignes haute tension, réseau élec |
| Météo-France / DRIAS / Climadiag | Climat actuel (normales 1991-2020) + projections 2050/2100 |
| GéoLittoral / BDIFF | Érosion côtière, historique feux de forêt |
| Géoplateforme WFS | Servitudes (SUP), Natura 2000, ZNIEFF, sites classés, UNESCO, PEB |
| data.culture.gouv.fr | Monuments historiques, SPR (périmètres ABF) |
| ARCEP | Fibre (par adresse), couverture mobile |
| SISPEA / EauFrance | Eau potable, assainissement (collectif/non collectif) |
| INSEE BPE + FINESS + data.education | Commerces, santé, écoles |
| Atmo Data / Geod'air | Qualité de l'air (indice ATMO par commune, concentrations) |
| Cerema CBS | Cartes de bruit stratégiques (routes/rails) |
| Hub'Eau | Eau souterraine |
| ADEME | DPE (énergie) |
| Carte des loyers | Loyers par commune |
| REI DGFiP | Taxe foncière |
| OSM / Overpass | POI, transport, bornes incendie |
| IGN Géocodage | Adresses, itinéraires |

---

## 13. Modèle de données

> **Note PostGIS (27.3)** : chaque colonne `geometry` (EPSG:4326) possède une colonne compagnon `*_lambert_93` (EPSG:2154) pour les calculs métriques (distances, surfaces). Les deux sont indexées GiST/B-tree. Non répétées dans les tables ci-dessous.
>
> **Note colonnes (27.2)** : toute donnée filtrable/triable/scorée est une colonne dédiée indexée. Les JSONB listés ici sont display-only ou paramétrage (jamais filtrés).
>
> **Note nommage (27.27)** : tous les identifiants (tables, colonnes, enums, valeurs stockées) sont en anglais, mots complets, unités épelées avec le motif `_in_`. La prose de la spec reste française ; seuls les identifiants techniques sont anglais.

### Table `users`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| email | TEXT | Email (unique) |
| last_name | TEXT | Nom |
| first_name | TEXT | Prénom |
| account_type | ENUM | individual / agency / notary |
| siret | TEXT | SIRET (si pro) |
| role | ENUM | user / moderator / admin (défaut: user — backoffice wave-08) |
| is_blocked | BOOLEAN | Compte désactivé par modération (récupérable) |
| email_verified | BOOLEAN | Email vérifié (attribut code `is_verified` — fastapi-users) |
| reliability_score | FLOAT | Score 0-100 (calculé automatiquement) |
| locale | TEXT | Préférence langue (défaut: 'fr') |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `projects`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK vers users — **NULL si projet local (déconnecté)**, renseigné à la sync (wave-09) |
| name | TEXT | Nom du projet |
| project_type | ENUM | housing / investment |
| category | ENUM | buried-terrain / classic-terrain / house / apartment (l'option "Terrain" en investissement = buried-terrain ou classic-terrain) |
| criteria | JSONB | Paramètres de recherche sauvegardés (config, pas filtré — voir 27.2) |
| zone | GEOMETRY(POLYGON, 4326) | Zone de recherche dessinée |
| zone_center | GEOMETRY(POINT, 4326) | Centre si recherche par rayon |
| zone_radius_in_kilometers | FLOAT | Rayon si recherche circulaire |
| max_budget_in_euros | FLOAT | Budget maximum |
| latest_results | JSONB | IDs des résultats sauvegardés (détection nouvelles offres) |
| new_offers_count | INT | Nombre de nouvelles offres |
| created_at | TIMESTAMPTZ | |
| last_viewed_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `priority_zones`

Zones de priorité dessinées sur la carte investissement (wave-04). Plusieurs par projet.

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| project_id | UUID | FK vers projects |
| level | ENUM | high / medium / low |
| geometry | GEOMETRY(POLYGON, 4326) | Polygone de la zone (compagnon _lambert_93) |
| created_at | TIMESTAMPTZ | |

### Table `weighting_profiles`

Profils de pondération sauvegardés (wave-04). Par utilisateur, réutilisables sur plusieurs projets.

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK vers users |
| name | TEXT | Nom du profil |
| category | ENUM | buried-terrain / classic-terrain / house / apartment |
| weights | JSONB | {critere: poids} — somme = 100 (config, pas filtré — 27.2) |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `terrains`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| parcel_id | TEXT | Identifiant cadastre (14 car.) |
| commune | TEXT | Code INSEE + nom |
| surface_in_square_meters | FLOAT | Surface en m² |
| geometry | GEOMETRY(POLYGON, 4326) | Géométrie PostGIS |
| zone | ENUM | urban / periurban / rural |
| buildable | BOOLEAN | Constructible selon PLU |
| estimated_price_in_euros | FLOAT | Prix estimé (DVF) |
| property_tax_in_euros | FLOAT | Taxe foncière annuelle moyenne (REI DGFiP) |
| slope_in_percent | FLOAT | Pente moyenne (%) |
| exposure | TEXT | Exposition (N/NE/E/SE/S/SW/W/NW) |
| metadata | JSONB | Données PLU, POI, etc. |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `properties`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| property_type | ENUM | house / apartment |
| address | TEXT | Adresse complète |
| commune | TEXT | Code INSEE + nom |
| surface_in_square_meters | FLOAT | Surface habitable |
| price_in_euros | FLOAT | Prix demandé |
| geometry | GEOMETRY(POINT, 4326) | Géocodage |
| energy_performance_class | TEXT | Étiquette énergie (A-G) |
| greenhouse_gas_class | TEXT | Étiquette GES (A-G) |
| potential_rent_in_euros | FLOAT | Loyer estimé/mois |
| property_tax_in_euros | FLOAT | Taxe foncière annuelle (REI DGFiP) |
| metadata | JSONB | DPE détaillé, POI, etc. |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `scores`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| target_type | ENUM | terrain / property |
| target_id | UUID | Cible polymorphe (terrain ou property) — pas de FK (une FK ne peut pas viser deux tables) |
| category | TEXT | buried-terrain / classic-terrain / house / apartment |
| score | FLOAT | Score calculé (0-100) |
| breakdown | JSONB | Score par critère |
| computed_at | TIMESTAMPTZ | |

### Table `listings`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| owner_id | UUID | FK vers users (propriétaire de l'annonce) |
| listing_type | ENUM | terrain / house / apartment |
| status | ENUM | active / under_offer / sold / rented / archived / disabled / deleted / reported |
| address | TEXT | Adresse complète |
| commune | TEXT | Code INSEE + nom |
| geometry | GEOMETRY(POLYGON ou POINT, 4326) | Géométrie (polygone si terrain, point si maison/appt) |
| price_in_euros | FLOAT | Prix demandé |
| surface_in_square_meters | FLOAT | Surface |
| energy_performance_class | TEXT | Étiquette DPE (A-G) — colonne dédiée (27.2, filtrable) |
| bedrooms | INT | Nombre de chambres (house/apartment) — colonne dédiée (27.2) |
| photos | JSONB | [{url, order, main}] — URLs S3 uniquement, jamais de binaires (27.2) |
| features | JSONB | Champs spécifiques display-only (agency_fees, charges, availability…) |
| description | TEXT | Description libre |
| source | ENUM | manual / import / claim |
| claim_status | ENUM | none / pending / approved / rejected (aligné sur claims.status) |
| submitted_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| last_verified_at | TIMESTAMPTZ | |
| report_count | INT | Nombre de signalements reçus |

### Table `reports`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| listing_id | UUID | FK vers listings |
| user_id | UUID | FK vers users (nullable si déconnecté) |
| device_fingerprint | TEXT | Hash du navigateur (pour déconnecté) |
| report_type | ENUM | sold / under_offer / fraud / price_error / other |
| message | TEXT | Message libre (optionnel) |
| status | ENUM | pending / processed / rejected (modération wave-08) |
| created_at | TIMESTAMPTZ | |

### Table `claims`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| listing_id | UUID | FK vers listings |
| user_id | UUID | FK vers users (requérant) |
| claim_type | ENUM | owner / agent / agency / notary |
| proof_document_url | TEXT | URL du justificatif uploadé |
| status | ENUM | pending / approved / rejected |
| admin_note | TEXT | Commentaire admin |
| created_at | TIMESTAMPTZ | |
| resolved_at | TIMESTAMPTZ | |

### Table `feedback`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK vers users — NULL si déconnecté (27.26) |
| tracking_token | TEXT | Token de suivi local (si non connecté — 27.26) |
| feedback_type | ENUM | bug / idea / question / complaint |
| message | TEXT | Contenu du feedback |
| page | TEXT | Page où le feedback a été fait |
| context | JSONB | Données contextuelles (projet courant, filtres, etc.) |
| status | ENUM | new / in_progress / processed / archived |
| response | TEXT | Réponse de l'équipe (si applicable) |
| user_agent | TEXT | Navigateur / device |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `contacts`

Messages acheteur → vendeur (wave-03, contact vendeur). Rate limiting via Redis (27.8) : 5 messages/heure.

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| listing_id | UUID | FK vers listings |
| sender_id | UUID | FK vers users (connecté obligatoire) |
| message | TEXT | Contenu du message |
| is_read | BOOLEAN | Lu par le vendeur |
| created_at | TIMESTAMPTZ | |

### Table `favorites`

Propriétés/terrains favoris (wave-02). Cible polymorphe (terrain ou property).

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK vers users |
| target_type | ENUM | terrain / property (aligné sur scores.target_type) |
| target_id | UUID | Cible polymorphe (terrain ou property) — pas de FK |
| project_id | UUID | FK vers projects (nullable — favori hors projet) |
| notes | TEXT | Notes personnelles (optionnel) |
| created_at | TIMESTAMPTZ | |

### Table `shares`

Liens de partage par token (wave-02 : projet / comparatif / carte).

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| token | TEXT | Token public (unique, indexé) |
| share_type | ENUM | project / comparison / map |
| user_id | UUID | FK vers users (créateur) |
| target_id | UUID | ID de l'objet partagé |
| expires_at | TIMESTAMPTZ | Expiration (défaut 30j) |
| revoked | BOOLEAN | Révoqué par le créateur |
| created_at | TIMESTAMPTZ | |

### Table `notifications`

Notifications in-app (wave-07 — définition canonique déplacée ici).

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK vers users |
| notification_type | ENUM | new_offer / update / listing_status / report / contact / account / weekly_digest |
| title | TEXT | Titre |
| message | TEXT | Corps |
| link | TEXT | URL relative de destination |
| is_read | BOOLEAN | Lue |
| created_at | TIMESTAMPTZ | |

---

## 13. Architecture backend

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings (env vars)
│   ├── api/
│   │   ├── projets.py       # CRUD projets
│   │   ├── terrains.py      # Endpoints terrains
│   │   ├── biens.py         # Endpoints biens (maison/appt)
│   │   ├── search.py        # Recherche géo
│   │   ├── scoring.py       # Endpoint scoring
│   │   ├── layers.py        # Calques investissement
│   │   ├── feedback.py      # Canal feedback utilisateurs
│   │   ├── annonces.py      # CRUD annonces
│   │   ├── contacts.py      # Contact vendeur (wave-03)
│   ├── core/
│   │   ├── scoring.py       # Moteur de scoring (par catégorie)
│   │   ├── geocoding.py     # Géocodage / reverse geocodage (seul appel externe runtime — 27.9)
│   │   ├── filters.py       # Filtrage par catégorie
│   │   └── new_offers.py    # Détection nouvelles offres
│   ├── db/
│   │   ├── models.py        # SQLAlchemy + GeoAlchemy2
│   │   └── session.py       # DB connection
│   └── schemas/
│       ├── projet.py        # Pydantic models projets
│       ├── terrain.py       # Pydantic models terrains
│       ├── bien.py          # Pydantic models biens
│       └── scoring.py       # Scoring models
├── alembic/                 # Migrations
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

> **Données open data (27.9/27.10)** : il n'y a PAS de clients runtime vers les APIs externes (cadastre, DVF, Géorisques, ADEME…). Toutes ces sources sont répliquées en local par les pipelines **Airflow + dbt** (ingestion/), qui remplissent les tables du modèle ci-dessus. Le seul appel externe runtime est le géocodage IGN (`core/geocoding.py`).

### Endpoints API

```
# Projets
GET    /api/projets                    # Liste mes projets
POST   /api/projets                    # Créer un projet
GET    /api/projets/{id}               # Détail projet
PUT    /api/projets/{id}               # Modifier un projet
DELETE /api/projets/{id}               # Supprimer un projet
POST   /api/projets/{id}/duplicate     # Dupliquer un projet
GET    /api/projets/{id}/new-offers    # Nombre nouvelles offres
POST   /api/projets/{id}/load          # Charger résultats du projet

# Terrains
GET    /api/terrains                    # Liste filtrée
GET    /api/terrains/{id}               # Détail
POST   /api/terrains/search             # Recherche géo
POST   /api/terrains/score              # Scoring
GET    /api/terrains/{id}/risks         # Risques
GET    /api/terrains/{id}/exposition    # Analyse exposition
GET    /api/terrains/{id}/pente         # Analyse pente

# Biens (maison / appartement)
GET    /api/biens                       # Liste filtrée
GET    /api/biens/{id}                  # Détail
POST   /api/biens/search                # Recherche
POST   /api/biens/analyze               # Analyse investissement
GET    /api/biens/{id}/dpe              # Données énergie

# Calques investissement
GET    /api/layers/rentabilite          # Heatmap rentabilité
GET    /api/layers/prix-m2              # Heatmap prix/m²
GET    /api/layers/loyers               # Heatmap loyers
GET    /api/layers/transport            # Isochrone transport
GET    /api/layers/risques              # Overlay risques
GET    /api/layers/dpe                  # Points DPE

# Commun
GET    /api/geocoding/search            # Géocodage
GET    /api/geocoding/reverse           # Reverse geocodage
GET    /api/stats                       # Stats marché

# Feedback
POST   /api/feedback                    # Envoyer un feedback
GET    /api/feedback                    # Lister les feedbacks (admin)
PUT    /api/feedback/{id}/status        # Modifier le statut (admin)

# Annonces
POST   /api/annonces                    # Créer une annonce
GET    /api/annonces/{id}               # Détail annonce
PUT    /api/annonces/{id}               # Modifier une annonce
DELETE /api/annonces/{id}               # Supprimer une annonce
PUT    /api/annonces/{id}/statut        # Changer le statut (vendu, loué, etc.)
POST   /api/annonces/{id}/signal        # Signaler comme indisponible
POST   /api/annonces/{id}/claim         # Récupérer un bien existant
GET    /api/mes-annonces                # Mes annonces (propriétaire)
```

---

## 12. Architecture frontend

```
frontend/
├── src/
│   ├── routes/
│   │   ├── +layout.svelte                  # Layout principal
│   │   ├── +page.svelte                    # Home : liste projets + mes annonces
│   │   │
│   │   ├── projet/
│   │   │   └── nouveau/
│   │   │       └── +page.svelte            # Wizard création
│   │   │
│   │   ├── annonce/
│   │   │   ├── deposer/
│   │   │   │   └── +page.svelte            # Wizard dépôt annonce
│   │   │   └── [id]/
│   │   │       └── +page.svelte            # Fiche annonce
│   │   │
│   │   ├── logement/
│   │   │   ├── +layout.svelte              # Layout logement
│   │   │   ├── terrain-terre/
│   │   │   │   ├── +page.svelte            # Carte + filtres
│   │   │   │   └── [id]/
│   │   │   │       └── +page.svelte        # Fiche détaillée
│   │   │   ├── terrain-classique/
│   │   │   │   ├── +page.svelte
│   │   │   │   └── [id]/
│   │   │   │       └── +page.svelte
│   │   │   ├── maison/
│   │   │   │   ├── +page.svelte
│   │   │   │   └── [id]/
│   │   │   │       └── +page.svelte
│   │   │   └── appartement/
│   │   │       ├── +page.svelte
│   │   │       └── [id]/
│   │   │           └── +page.svelte
│   │   │
│   │   └── investir/
│   │       ├── +layout.svelte              # Layout investissement
│   │       ├── maison/
│   │       │   ├── +page.svelte            # Carte + calques
│   │       │   └── [id]/
│   │       │       └── +page.svelte        # Fiche analyse
│   │       ├── appartement/
│   │       │   ├── +page.svelte
│   │       │   └── [id]/
│   │       │       └── +page.svelte
│   │       └── terrain/
│   │           ├── +page.svelte
│   │           └── [id]/
│   │               └── +page.svelte
│   │
│   ├── lib/
│   │   ├── components/
│   │   │   ├── Map.svelte                  # Carte MapLibre wrapper
│   │   │   ├── TerrainCard.svelte          # Card terrain
│   │   │   ├── BienCard.svelte             # Card bien
│   │   │   ├── ProjetCard.svelte           # Card projet (home)
│   │   │   ├── ScoreRing.svelte            # Visualisation score
│   │   │   ├── FilterPanel.svelte          # Filtres lateraux
│   │   │   ├── LayerToggle.svelte          # Toggle calques
│   │   │   ├── DrawingTools.svelte         # Outils dessin zone (polygone, rectangle, cercle, gomme, reset)
│   │   │   ├── PriorityZones.svelte       # Gestion zones de priorité (rouge/orange/vert)
│   │   │   ├── WeightSliders.svelte       # Pondération critères (sliders interactifs)
│   │   │   ├── FeedbackWidget.svelte     # Widget feedback in-app (bulle flottante)
│   │   │   ├── AnnonceForm.svelte        # Formulaire dépôt annonce
│   │   │   ├── AnnonceCard.svelte        # Card annonce (liste)
│   │   │   ├── ClaimModal.svelte         # Modal récupération bien
│   │   │   ├── SignalModal.svelte        # Modal signalement (connecté/déconnecté)
│   │   │   ├── WizardStep.svelte           # Étape wizard
│   │   │   ├── CompareTable.svelte         # Table comparatif
│   │   │   └── LanguageSwitcher.svelte    # Sélecteur FR/EN
│   │   ├── i18n/
│   │   │   ├── fr.json                    # Traductions FR
│   │   │   ├── en.json                    # Traductions EN
│   │   │   └── index.ts                   # Config Paraglide
│   │   ├── stores/
│   │   │   ├── projets.ts                  # Store projets
│   │   │   ├── terrains.ts                 # Store terrains
│   │   │   ├── biens.ts                    # Store biens
│   │   │   ├── filters.ts                  # Store filtres
│   │   │   └── layers.ts                   # Store calques
│   │   └── api/
│   │       └── client.ts                   # Fetch wrapper
│   └── app.html
├── svelte.config.js
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## 20. Authentification & profils

### Providers d'authentification

| Provider | Priorité | Notes |
|---|---|---|
| Email + mot de passe | P0 | Vérification email obligatoire |
| Google OAuth | P1 | "Se connecter avec Google" |
| Apple Sign In | P2 | Obligatoire si app iOS |
| GitHub OAuth | P3 | Pour les développeurs / early adopters |

### Flow d'inscription

```
[1] Email + MDP ─── [2] Vérification email ─── [3] Profil (optionnel)
     ●                      ○                        ○
```

- **Étape 1** : Email + mot de passe (min 8 car., 1 majuscule, 1 chiffre)
- **Étape 2** : Email de vérification (lien à usage unique, expire 24h)
- **Étape 3** : Nom, prénom, type (particulier/agence/notaire), SIRET (si pro)

### Flow de connexion

- Email + mot de passe
- Ou provider OAuth → redirect automatique
- "Mot de passe oublié" → email de reset (lien à usage unique, expire 1h)

### Sécurité

| Mesure | Description |
|---|---|
| Rate limiting | 5 tentatives/15min par email |
| Lockout | 30 min après 5 échecs consécutifs |
| JWT | Access token (15min) + Refresh token (7 jours) |
| HttpOnly cookies | Tokens stockés en httpOnly, pas localStorage |
| CSRF | Protection CSRF sur les routes stateful |

### Table `users` (mise à jour)

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| email | TEXT | Email (unique) |
| password_hash | TEXT | Hash bcrypt (null si OAuth only) |
| nom | TEXT | Nom |
| prenom | TEXT | Prénom |
| type | ENUM | particulier / agence / notaire |
| siret | TEXT | SIRET (si pro) |
| email_verifie | BOOLEAN | Email vérifié |
| score_fiabilite | FLOAT | Score 0-100 |
| locale | TEXT | Préférence langue (défaut: 'fr') |
| avatar_url | TEXT | Photo de profil (optionnel) |
| provider | TEXT | 'local', 'google', 'apple', 'github' |
| provider_id | TEXT | ID externe (si OAuth) |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| last_login_at | TIMESTAMPTZ | Dernière connexion |

---

## 21. Mobile & responsive

### Stratégie

Plot est une application **mobile-first**. 60%+ du trafic immobilier vient du mobile.

### Breakpoints

| Taille | Breakpoint | Layout |
|---|---|---|
| Mobile | < 768px | Single column, carte plein écran, filtres en bottom sheet |
| Tablette | 768-1024px | 2 colonnes, filtres sidebar rétractable |
| Desktop | > 1024px | Layout complet (sidebar + carte + résultats) |

### Comportements mobile

| Élément | Comportement |
|---|---|
| Carte | Plein écran, filtres en overlay |
| Filtres | Bottom sheet (swipe up) |
| Résultats | Liste en dessous de la carte (scroll vertical) |
| Wizard | Plein écran, navigation par swipe ou boutons |
| Fiche détaillée | Plein écran avec retour |
| Navigation | Bottom bar (accueil, projets, carte, profil) |

### Touch

| Gesture | Action |
|---|---|
| Pinch to zoom | Zoom carte |
| Swipe left/right | Naviguer entre résultats |
| Pull down | Rafraîchir |
| Long press | Marquer favori |

---

## 22. RGPD & légal

### Conformité RGPD

| Exigence | Implémentation |
|---|---|
| Consentement cookies | Banner cookie (Plausible compliant) |
| Droit d'accès | Export de toutes les données utilisateur (JSON) |
| Droit de rectification | Profil modifiable depuis les settings |
| Droit à l'effacement | Suppression de compte (avec confirmation) |
| Portabilité | Export JSON des projets, favoris, annonces |
| Minimisation des données | Seules les données nécessaires sont collectées |

### Durée de rétention

| Donnée | Rétention |
|---|---|
| Compte utilisateur | Jusqu'à suppression par l'utilisateur |
| Annonces supprimées | 30 jours (récupération possible) |
| Projets archivés | 1 an |
| Logs de connexion | 1 an |
| Signalements | 2 ans |
| Feedback | 2 ans |
| Notifications | Supprimées après 90 jours (lues) ou 1 an (non lues) |
| Favoris | Jusqu'à suppression par l'utilisateur |
| Claims | 2 ans après résolution |
| Messages (contacts) | 2 ans |
| Cookies | 13 mois max |

### Mentions légales

- **Éditeur** : nom, adresse, SIRET
- **Hébergeur** : nom, adresse
- **Contact DPO** : email dédié
- **Politique de confidentialité** : `/fr/mentions-legales`
- **CGU** : `/fr/conditions-generales`

### Cookies

| Cookie | Finalité | Durée | Consentement |
|---|---|---|---|
| session | Authentification | Session | Non (strictement nécessaire) |
| locale | Préférence langue | 1 an | Non (fonctionnel) |
| analytics | Statistiques anonymisées | 13 mois | Oui (optionnel) |

---

## 23. Analytics

### Outil : Plausible Analytics

- Self-hosted ou cloud (plausible.io)
- Respectueux de la vie privée (pas de cookies, RGPD compliant)
- Pas de consentement nécessaire

### Événements trackés

| Événement | Description |
|---|---|
| `pageview` | Page visitée |
| `project_create` | Nouveau projet créé |
| `project_load` | Projet chargé |
| `annonce_create` | Annonce déposée |
| `annonce_view` | Fiche consultée |
| `filter_apply` | Filtre appliqué |
| `drawing_zone` | Zone dessinée |
| `contact_vendor` | Contact vendeur |
| `share` | Lien de partage généré |
| `feedback_submit` | Feedback envoyé |

---

## 24. SEO

### Stratégie

- **SSR** avec SvelteKit (rendu côté serveur)
- **Sitemap dynamique** généré automatiquement
- **Meta tags** dynamiques par page
- **Structured data** (JSON-LD) pour les annonces

### Routes publiques (indexées)

| Route | Meta |
|---|---|
| `/` | "Plot — Trouvez le meilleur logement en France" |
| `/logement/terrain-terre` | "Terrain pour maison enterrée" |
| `/logement/terrain-classique` | "Terrain construction classique" |
| `/logement/maison` | "Maison à vendre" |
| `/logement/appartement` | "Appartement à vendre" |
| `/investir/maison` | "Investissement locatif maison" |
| `/investir/appartement` | "Investissement locatif appartement" |
| `/annonce/[id]` | Fiche bien (title dynamique) |

### Landing pages (villes)

Générées dynamiquement pour les villes avec annonces :
- `/fr/maisons-a-vendre/paris`
- `/fr/terrains-a-vendre/aude`
- etc.

---

## 25. Monitoring

### Stack

| Outil | Usage |
|---|---|
| Sentry | Erreurs frontend + backend |
| Uptime Kuma | Surveillance uptime |
| Plausible | Analytics |

### Alertes

| Alerte | Seuil | Canal |
|---|---|---|
| Erreur 5xx | > 5/5min | Email |
| Temps réponse API | > 2s (p95) | Email |
| CPU serveur | > 80% 5min | Email |
| Espace disque | > 80% | Email |
| Nouveau feedback "bug" | Immédiat | Email |

---

## 26. CI/CD

### Pipeline

```
Push → Lint → TypeCheck → Tests → Build → Deploy
```

### Environments

| Env | Branch | Deploy |
|---|---|---|
| Development | `develop` | Auto |
| Staging | `main` | Auto |
| Production | `main` | Manual |

### Checks avant merge

- [ ] Lint (Biome)
- [ ] TypeCheck (TypeScript strict)
- [ ] Tests (Vitest)
- [ ] Build (SvelteKit)
- [ ] Review (1 minimum)

---

## 27. Décisions d'architecture

> Décisions validées lors de la maturation Wave 01 (checklist 8 critères).

### 27.1 Données : OpenData vs Annonces (Q1-Q2)

**Pattern Hybrid** : les données open data (`terrains`, `biens`) et les annonces utilisateurs (`annonces`) sont dans des tables séparées. La couche API **fusionne à la lecture** : chaque terrain/bien peut avoir 0 ou 1 annonce associée.

| État | Affichage |
|---|---|
| Terrain/bien sans annonce | Read-only (données open data) |
| Terrain/bien avec annonce | Enrichi (prix vendeur, photos, description) |

Pas de fusion en écriture. L'ETL remplit les tables open data. Les annonces sont créées par les utilisateurs. L'API joint les deux au moment de la requête.

### 27.2 Données : JSONB vs colonnes dédiées (Q3) + photos

**Principe directeur** : une donnée utilisée dans le WHERE (filtre), le ORDER BY (tri), ou le scoring (calcul de score) DOIT être une colonne dédiée indexée. Le JSONB est réservé aux données **display-only** (jamais filtrées, jamais triées, jamais scorées).

| Donnée | Modèle |
|---|---|
| Surface, prix, pente, exposition, buildable, zone, DPE, loyer, taxe foncière | Colonne dédiée + index B-tree |
| Géométrie (parcelle, zone, point) | Colonne GEO dédiée (PostGIS geometry) — jamais dans JSONB |
| Extractions depuis JSONB source | Colonnes virtuelles `GENERATED ALWAYS AS ... STORED` |
| Metadata enrichissement (POI, PLU raw) | JSONB (display-only) |
| Full-text / texte libre | JSONB GIN index (uniquement si recherche libre) |

Le scoring travaille sur des colonnes (matériau pré-calculé + index), cohérent avec la table `scores`.

**Photos** : stockées dans un **gestionnaire de fichiers objet (S3-compatible)**, jamais en base. Le champ `photos` en base ne contient que des **références/URLs** vers l'objet — pas les binaires.

### 27.3 PostGIS : système de coordonnées (Q4)

**Double stockage** :
- `geometry` en **EPSG:4326** (WGS84) pour MapLibre GL JS
- `geometry_lambert_93` en **EPSG:2154** (RGF93 Lambert-93) pour les calculs de distance et surface (27.27 : nommage auto-documenté)

PostGIS gère les conversions via `ST_Transform()`. Les deux colonnes sont indexées.

### 27.4 PostGIS : géométries invalides (Q5)

**Auto-correction à l'import** : l'ETL applique `ST_MakeValid()` + log `ST_IsValidReason()` avant insertion. Les géométries invalides sont corrigées automatiquement. Les logs enregistrent les corrections pour suivi.

### 27.5 PostGIS : recherche spatiale (Q6)

**GiST index natif** sans clustering. Le GiST fait du bbox pre-filtering nativement. Architecture des requêtes :

| Canal | Mécanisme |
|---|---|
| Carto web (MapLibre) | Tile server (Martin/pg_tileserv) → cache tuiles → PostGIS |
| Recherche zone dessinée | FastAPI → GiST index → PostGIS |
| Enrichissement annonce | FastAPI → GiST index → PostGIS |

Le clustering sera évalué si les benchmarks montrent des lenteurs > 500ms.

### 27.6 Auth : conflit email OAuth (Q7)

**Erreur + lien manuel** : si un compte local existe déjà avec l'email OAuth, un message d'erreur indique à l'utilisateur de se connecter en local puis de lier son compte OAuth dans les settings. Pas de merge automatique (risque de sécurité).

### 27.7 Auth : account enumeration (Q8)

**Messages séparés + rate limiting strict** : les messages d'erreur distinguent "email inconnu" de "mauvais mot de passe", mais le rate limiting (Q9) rend l'enumeration impraticable en pratique.

### 27.8 Auth : rate limiting (Q9)

**Double limite IP + email** en Redis :

| Clé Redis | TTL | Max | Scope |
|---|---|---|---|
| `rl:login:{email_hash}` | 15 min | 5 | Par email |
| `rl:login:{ip}` | 15 min | 5 | Par IP |

Les emails sont hashés dans les clés Redis (PII-safe).

### 27.9 Sources : données locales vs API temps réel (Q10)

**Réplication totale** : toutes les données open data sont répliquées en local via ETL (Airflow + dbt). Aucune API externe n'est requêtée en runtime, sauf :

| API temps réel | Usage |
|---|---|
| IGN Géocodage | Résolution adresse → coordonnées |
| IGN Reverse Géocodage | Clic carte → adresse |

La fraîcheur devient un problème ETL (refresh daily/weekly), pas runtime.

### 27.10 Pipeline d'ingestion (Q11)

**Full platform : Airflow + dbt** pour l'orchestration des pipelines ETL. Chaque source a son propre pipeline avec :
- Rate limiter spécifique (respect des contraintes provider)
- Retry + backoff exponentiel
- Logging + monitoring
- Fréquence adaptée à la source (annuel, trimestriel, mensuel, hebdo)

### 27.11 Données manquantes (Q12)

**Scoring sur données disponibles** : le scoring ignore les critères sans données. L'UI affiche "Donnée non disponible" pour les champs manquants. Le score est indicatif, pas absolu.

### 27.12 Signalement déconnecté (Q13)

**Mode hybride** :
- **En ligne** (non logué) : signal envoyé directement au serveur (anonyme + device_fingerprint)
- **Hors-ligne** (PWA) : signal stocké en localStorage + sync au retour en ligne via Background Sync API

### 27.13 Infra production (Q14)

**Docker Compose dev + ECS/Railway prod** :

| Environnement | Outil | Purpose |
|---|---|---|
| Dev | Docker Compose | Stack locale complète |
| Prod | Railway ou ECS Fargate | Managed, auto-scaling |

Stack prod : PostgreSQL+PostGIS, Redis, FastAPI, SvelteKit, Martin, Airflow, dbt, Plausible, Uptime Kuma.

### 27.14 Cache Redis (Q15)

**Architecture adoptée** : les tuiles vectorielles ne vont PAS dans Redis. Martin a un cache mémoire intégré (Moka LRU, 512 Mo) + benchmarks ~12,000 req/s @ z14 ; le bottleneck est le scoring/recherche polygon, pas les tuiles. Ajout d'un CDN avec purge + headers `Cache-Control` → le cache Martin suffit. Un cache Redis tuiles ne sert que si 2+ instances Martin (réviser plus tard).

**Redis (4 Go, `allkeys-lru`) cache** :
| Cache | Key | TTL | Invalidation |
|---|---|---|---|
| Scores par parcelle | `scores:v{N}:{parcel_id}` | 7j | Airflow INCR version |
| Résultats recherche | `search:v{N}:h3:{cell}` | 1h | Tags (SMEMBERS+UNLINK) |
| Rate limiting IP+email | `rl:ip:{ip}` / `rl:email:{email}` | 15 min (fenêtre) | Fenêtre glissante |

- Normalisation par grille **H3** pour les résultats de recherche (stocker IDs+scores, géométrie servie par les tuiles)
- cache-aside, `orjson` + compression `zlib`/`zstd`, **fail-open** sur erreur Redis (jamais 500 si Redis down)
- Sizing 4 Go, hit rate monitoré (>30-60% = bug de normalization de clé)
- **Géocodage non caché** (réponses uniques, hit rate ≈ 0)

**Invalidation ETL** : Airflow/dbt post-ETL → `INCR cache:version:{dataset}` (scores, parcels, biens) + purge CDN. TTL comme safety net si le hook échoue. Tapotage via couches versionnées (O(1)) + tags (spatial) + TTL.

**Tiles** : `Cache-Control: public, max-age=86400` (cache navigateur L1) + CDN purge sur ETL + Martin `cache.expiry` = cadence ETL.

### 27.15 Alembic migrations (Q16)

**Migrations incrémentales** : un fichier par changement, `alembic revision --autogenerate` détecte les changements SQLAlchemy. Standard FastAPI, history claire.

### 27.16 RGPD effacement (Q17)

**Suppression complète + anonymisation** : le compte utilisateur et toutes les données personnelles (annonces, signalements, feedback, scores liés) sont supprimés. Les données agrégées anonymisées restent (stats marché non rattachables à un user).

### 27.17 Traductions manquantes (Q18)

**Build error** : Paraglide détecte les clés manquantes en EN au build time. Le build échoue avec la liste des clés manquantes. Force la complétude des traductions avant déploiement.

### 27.18 Validation UX pré-frontend

**Règle** : avant de démarrer l'implémentation de chaque parcours utilisateur frontend, valider l'UX wireframe/prototype par parcours. Chaque parcours (recherche terrain, recherche maison, dépôt annonce, investissement, signalement, etc.) a un livrable UX validé avant le code.

### 27.19 Personas futurs

Deux personas supplémentaires à intégrer dans une future wave :
- **Bailleur** (landlord) : gestion des bails, état des lieux, quittancement
- **Locataire** (tenant) : recherche de location, état des lieux, droits

### 27.20 Backup & disaster recovery (PRA)

| Élément | Stratégie |
|---|---|
| PostgreSQL | Snapshot quotidien (managed provider) + WAL continu (PITR, RPO ≤ 15 min) |
| Redis | Aucun backup (cache pur — reconstruit depuis PostGIS) |
| Photos S3 | Réplication gérée par le provider (durabilité 11×9) |
| Airflow/dbt | Rejouable : les pipelines reconstruisent les données depuis les sources |
| Restore test | Mensuel : restauration sur environnement de staging |
| RTO cible | ≤ 4 h (redéploiement + restore PITR) |

### 27.21 Accessibilité

- **Cible** : RGAA 4.1 niveau AA (= WCAG 2.1 AA)
- **Priorités** : navigation clavier complète, contrastes AA, focus visible, formulaires labellisés, tailles de cible tactile ≥ 44px, résumé textuel des résultats carte (MapLibre)
- **Tests** : axe-core en CI, audit manuel annuel
- **Déclaration** : page `/fr/accessibilite` (déclaration RGAA obligatoire dès publication)

### 27.22 Trigger "nouvelles offres" (Q1 — hybride)

- **Annonces utilisateur** (dépôt/modification) : webhook interne → matching immédiat contre les projets actifs → notification. La fréquence "Instantané" de wave-07 ne s'applique qu'à ce canal.
- **Données ETL** : matching exécuté au refresh ETL (batch). La détection vit dans `core/new_offers.py`, déclenchée par les deux canaux ; le compteur `projets.nouvelles_offres` et les notifications wave-07 partagent le même matching.

### 27.23 Espace annonceur (Q2 — wave dédiée)

**Dashboard complet** → **wave-11-espace-annonceur** : mes annonces, boîte de contacts (réponse inline), stats vues, score de fiabilité visible. Impact fiabilité du contact : **+1/mois si taux de réponse > 80 % sous 72 h** (donnée : table `contacts`, champ `lu` + réponses).

### 27.24 Réconciliation signalements anonymes → compte (Q3 — rattachement auto)

À la création de compte, le serveur **rattache automatiquement** au nouveau `user_id` les signalements et masquages associés au `device_fingerprint` (signalements anonymes serveur + files de sync locale). Le masquage suit ensuite le compte (multi-device). Deux mécanismes coexistant : Background Sync = transport device→serveur ; le rattachement = attribution compte, indépendant.

### 27.25 Modération & anti-abus (Q4 — wave dédiée avec analyse préalable)

**wave-12-moderation-antabuse**. Une **analyse préalable est obligatoire** avant toute spécification : volume attendu de signalements, seuils d'escalade vs charge de modération, définition du signalement abusif, score signaleur, RGPD des pénalités. La file de modération unifiée et l'anti-abus signaleur seront spécifiés à l'issue de l'analyse.

### 27.26 Feedback : identité et suivi (Q5 — hybride)

- **user_id** si connecté, sinon **token_suivi** local (comme les projets locaux)
- Endpoint `GET /api/feedback/mine` : l'utilisateur suit le statut de ses feedbacks (statut + réponse)
- Notification in-app à la réponse de l'équipe (type `compte` ou dédié — wave-07)
- "Convertir en issue GitHub" : action **manuelle** de l'admin (pas d'intégration automatisée)

### 27.27 Convention de nommage (full English)

Décision utilisateur (2026-09-01) : **tout identifiant technique est en anglais** — mots complets, sans abréviation inventée. Seule la documentation produit (specs/, SPEC.md) reste en français.

- **Code (Python/TS)** : variables, fonctions, classes, attributs en anglais, révélant l'intention (`reliability_score`, pas `score_fiabilite` ni `score`). Abréviations interdites sauf conventions écosystème établies (`id`, `url`, `db`, module `deps` de FastAPI, alias `m` de Paraglide).
- **DB** : tables, colonnes, types et valeurs d'enum en anglais (`listings`, `properties`, `reports`, `priority_zones`, `weighting_profiles`, `favorites`, `shares`, `energy_performance_class`, `email_verified`, valeurs `"rented"`, `"high"`, `"under_offer"`...). Les unités sont épelées avec le motif `_in_` (`price_in_euros`, `surface_in_square_meters`, `zone_radius_in_kilometers`, `slope_in_percent`).
- **Noms propres administratifs français conservés** : ce sont des noms officiels, pas des abréviations (`siret`, `commune`, `insee`, `plu`, `dvf`).
- **Géométries (27.3 révisé)** : compagnon métrique `*_lambert_93` (EPSG:2154) au lieu de `*_2154` — nom de projection officiel auto-documenté.
- **Enums** : classes/membres/valeurs anglais (`ListingStatus.RENTED`), la traduction UI se fait côté Paraglide (contenu vs libellés).
- **Docs** : specs/ + SPEC.md en français (référentiel produit) ; tout le reste (docs/, README, AGENTS.md, commentaires de code, PR) en anglais.
- **Garantir** : ruff `N` (pep8-naming) + `tests/test_naming.py` (liste noire noms vagues : `data`, `tmp`, `res`, `obj`...) côté Python ; Biome `namingConvention` + `naming.test.ts` côté TypeScript ; `.coderabbit.yaml` avec path_instructions "flag names that do not reveal intent".
