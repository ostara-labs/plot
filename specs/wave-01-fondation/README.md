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
| Cache | Redis |
| Emails | Postmark (transactionnel + digest) |
| SMS | SMSemode / Sarbacane (OTP, alertes) |
| Analytics | Plausible |
| Monitoring | Sentry + Uptime Kuma |
| i18n | Paraglide (SvelteKit) — FR/EN |
| Déploiement | Docker Compose (dev) → AWS / Railway (prod) |

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
| API Carto GPU | Zones constructibles PLU |
| IGN Altimétrie | Pente, exposition |
| Géorisques | Risques naturels |
| Hub'Eau | Eau souterraine |
| ADEME | DPE (énergie) |
| Carte des loyers | Loyers par commune |
| REI DGFiP | Taxe foncière |
| OSM / Overpass | POI, transport |
| IGN Géocodage | Adresses, itinéraires |

---

## 13. Modèle de données

### Table `users`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| email | TEXT | Email (unique) |
| nom | TEXT | Nom |
| prenom | TEXT | Prénom |
| type | ENUM | particulier / agence / notaire |
| siret | TEXT | SIRET (si pro) |
| email_verifie | BOOLEAN | Email vérifié |
| score_fiabilite | FLOAT | Score 0-100 (calculé automatiquement) |
| locale | TEXT | Préférence langue (défaut: 'fr') |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `projets`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| nom | TEXT | Nom du projet |
| type | ENUM | logement / investissement |
| categorie | TEXT | terrain-terre / terrain-classique / maison / appartement |
| criteres | JSONB | Critères de recherche (selon catégorie) |
| zone | GEOMETRY(POLYGON, 4326) | Zone de recherche dessinée |
| zone_centre | GEOMETRY(POINT, 4326) | Centre si recherche par rayon |
| zone_rayon_km | FLOAT | Rayon si recherche circulaire |
| budget_max | FLOAT | Budget maximum |
| derniers_resultats | JSONB | IDs des résultats sauvegardés |
| nouvelles_offres | INT | Nombre de nouvelles offres |
| date_creation | TIMESTAMPTZ | |
| date_derniere_consultation | TIMESTAMPTZ | |
| date_mise_a_jour | TIMESTAMPTZ | |

### Table `terrains`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| parcelle_id | TEXT | Identifiant cadastre (14 car.) |
| commune | TEXT | Code INSEE + nom |
| surface_m2 | FLOAT | Surface en m² |
| geometry | GEOMETRY(POLYGON, 4326) | Géométrie PostGIS |
| zone | ENUM | urbain / periurbain / rural |
| buildable | BOOLEAN | Constructible selon PLU |
| estimated_price_eur | FLOAT | Prix estimé (DVF) |
| slope_pct | FLOAT | Pente moyenne (%) |
| exposure | TEXT | Exposition (N/NE/E/SE/S/SW/W/NW) |
| metadata | JSONB | Données PLU, POI, etc. |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `biens`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| type | ENUM | maison / appartement |
| address | TEXT | Adresse complète |
| commune | TEXT | Code INSEE + nom |
| surface_m2 | FLOAT | Surface habitable |
| price_eur | FLOAT | Prix demandé |
| geometry | GEOMETRY(POINT, 4326) | Géocodage |
| dpe | TEXT | Étiquette énergie (A-G) |
| ges | TEXT | Étiquette GES (A-G) |
| loyer_potentiel_eur | FLOAT | Loyer estimé/mois |
| metadata | JSONB | DPE détaillé, POI, etc. |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### Table `scores`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| target_type | ENUM | terrain / bien |
| target_id | UUID | FK vers terrains ou biens |
| category | TEXT | terrain-terre / terrain-classique / maison / appartement |
| score | FLOAT | Score calculé (0-100) |
| breakdown | JSONB | Score par critère |
| computed_at | TIMESTAMPTZ | |

### Table `annonces`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| owner_id | UUID | FK vers users (propriétaire de l'annonce) |
| type | ENUM | terrain / maison / appartement |
| statut | ENUM | active / sous_offre / vendu / loué / désactivée / supprimée / signalée |
| address | TEXT | Adresse complète |
| commune | TEXT | Code INSEE + nom |
| geometry | GEOMETRY(POLYGON ou POINT, 4326) | Géométrie (polygone si terrain, point si maison/appt) |
| price_eur | FLOAT | Prix demandé |
| surface_m2 | FLOAT | Surface |
| photos | JSONB | [{url, ordre, principale}] |
| caracteristiques | JSONB | Champs spécifiques au type (chambres, DPE, etc.) |
| description | TEXT | Description libre |
| source | ENUM | manuel / import / claim |
| claim_status | ENUM | none / pending / verified / rejected |
| date_depot | TIMESTAMPTZ | |
| date_mise_a_jour | TIMESTAMPTZ | |
| date_derniere_verification | TIMESTAMPTZ | |
| nombre_signalements | INT | Nombre de signalements reçus |

### Table `signalements`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| annonce_id | UUID | FK vers annonces |
| user_id | UUID | FK vers users (nullable si déconnecté) |
| device_fingerprint | TEXT | Hash du navigateur (pour déconnecté) |
| type | ENUM | vendu / sous_offre / faux / erreur_prix / autre |
| message | TEXT | Message libre (optionnel) |
| traite | BOOLEAN | Traité ou non |
| created_at | TIMESTAMPTZ | |

### Table `claims`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| annonce_id | UUID | FK vers annonces |
| user_id | UUID | FK vers users (requérant) |
| type | ENUM | proprietaire / mandataire / agence / notaire |
| justificatif_url | TEXT | URL du justificatif uploadé |
| status | ENUM | pending / approved / rejected |
| note_admin | TEXT | Commentaire admin |
| created_at | TIMESTAMPTZ | |
| resolved_at | TIMESTAMPTZ | |

### Table `feedback`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| type | ENUM | bug / idee / question / doléance |
| message | TEXT | Contenu du feedback |
| page | TEXT | Page où le feedback a été fait |
| context | JSONB | Données contextuelles (projet courant, filtres, etc.) |
| status | ENUM | nouveau / en_cours / traite / archive |
| reponse | TEXT | Réponse de l'équipe (si applicable) |
| user_agent | TEXT | Navigateur / device |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

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
│   │   └── sources.py       # Proxy vers sources externes
│   ├── core/
│   │   ├── scoring.py       # Moteur de scoring (par catégorie)
│   │   ├── geocoding.py     # Géocodage / reverse geocodage
│   │   ├── filters.py       # Filtrage par catégorie
│   │   └── new_offers.py    # Détection nouvelles offres
│   ├── data/
│   │   ├── cadastre.py      # Client API cadastre
│   │   ├── dvf.py           # Client DVF
│   │   ├── plu.py           # Client PLU
│   │   ├── poi.py           # Client OSM/Overpass
│   │   ├── risks.py         # Client Géorisques
│   │   ├── dpe.py           # Client ADEME DPE
│   │   ├── loyers.py        # Client loyers
│   │   └── altimetrie.py    # Client IGN altimétrie
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