# Plot — Spec

> Trouver le meilleur logement en France.

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
| Tile server | Martin (tuiles vectorielles PostGIS → MapLibre) |
| Cache / Rate limit | Redis |
| Ingestion ETL | Airflow + dbt (réplication open data locale — 27.9/27.10) |
| Emails | Postmark (transactionnel + digest) |
| SMS | SMSemode / Sarbacane (OTP, alertes) |
| Analytics | Plausible |
| Monitoring | Sentry + Uptime Kuma |
| i18n | Paraglide (SvelteKit) — FR/EN |
| Déploiement | Docker Compose (dev) → Railway / ECS Fargate (prod) |

---

## 3. Concepts clés

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

## Waves

Le spec est découpé en waves, chacune couvrant un domaine fonctionnel. Chaque wave est un fichier autonome qui référence le spec principal.

### Processus de maturation

Avant de commencer l'implémentation d'une wave, celle-ci doit être **mature**. La maturation consiste à s'assurer qu'il n'y a plus d'inconnu technique ou fonctionnel.

**Checklist de maturité :**

| Critère | Description |
|---|---|
| **Périmètre clair** | On sait exactement quoi implémenter, quoi ne pas implémenter |
| **Dépendances identifiées** | On sait quelles autres waves/externes sont nécessaires |
| **Données disponibles** | Les sources de données existent et sont accessibles |
| **API documentées** | Les APIs à consommer sont documentées |
| **Modèle de données défini** | Tables, colonnes, relations sont fixées |
| **Edge cas listés** | Les cas limites sont identifiés et des solutions proposées |
| **Pas de blocage technique** | Aucun spike technique nécessaire |
| **UI/UX validé** | Le layout et les interactions sont définis |

**Statuts wave :**

| Statut | Description |
|---|---|
| 🔜 À spécifier | Spec en cours de rédaction |
| ✅ Spécifié | Spec complète, pas encore mature |
| 🟡 Mature | Prête pour implémentation |
| 🔧 En cours | Implémentation en cours |
| ✅ Terminé | Livré |

### Table des waves

| Wave | Sujet | Statut |
|---|---|---|
| [Wave 01 — Fondation](wave-01-fondation/README.md) | Vision, stack, concepts clés, sources de données, modèle de données, architectures backend/frontend, i18n (FR/EN), auth, mobile, RGPD, analytics, SEO, monitoring, CI/CD | 🟡 Mature |
| [Wave 02 — Recherche](wave-02-recherche/README.md) | Page d'accueil, wizard de création, carte logement, critères d'évaluation, favoris, export PDF, partage | ✅ Spécifié |
| [Wave 03 — Annonces](wave-03-annonces/README.md) | Déposer une annonce, fiche détaillée, photos/médias, contact vendeur | ✅ Spécifié |
| [Wave 04 — Investissement](wave-04-investissement/README.md) | Carte investissement, calques, dessin de zone, priorités, pondération | ✅ Spécifié |
| [Wave 05 — Confiance](wave-05-confiance/README.md) | Signalement par les utilisateurs, score de fiabilité | ✅ Spécifié |
| [Wave 06 — Feedback](wave-06-feedback/README.md) | Feedback in-app | ✅ Spécifié |
| [Wave 07 — Notifications](wave-07-notifications/README.md) | Email, push, in-app, templates transactionnels | ✅ Spécifié |
| [Wave 08 — Backoffice](wave-08-backoffice/README.md) | Interface admin, modération, gestion users/signalements/feedbacks | ✅ Spécifié |
| [Wave 09 — PWA / Offline](wave-09-pwa-offline/README.md) | Service worker, cache, synchronisation, mode hors-ligne | ✅ Spécifié |
| [Wave 10 — Langues régionales](wave-10-langues-regionales/README.md) | Breton, occitan, basque, corse, alsacien, créoles | 🔜 À spécifier |
| [Wave 11 — Espace annonceur](wave-11-espace-annonceur/README.md) | Mes annonces, boîte contacts, stats, score fiabilité (27.23) | 🔜 À spécifier |
| [Wave 12 — Modération & anti-abus](wave-12-moderation-antabuse/README.md) | File de modération, interaction auto/manuel, anti-abus signaleur (27.25 — analyse préalable requise) | 🔬 Analyse préalable |

### Personas futurs

Deux personas supplémentaires à intégrer dans une **future wave** (non spécifiée à ce jour) :

| Persona | Besoins pressentis |
|---|---|
| **Bailleur** (landlord) | Gestion des bails, état des lieux, quittancement, suivi des loyers, fiscalité locative |
| **Locataire** (tenant) | Recherche de location, état des lieux d'entrée/sortie, suivi des droits, quittances |

Ces personas étendront le modèle `users` (actuellement `particulier` / `agence` / `notaire`) et ouvriront de nouveaux parcours, données et sous-produits. À murir dans une wave dédiée.

---

## 11. Pain points & idées d'adressage

Recherche basée sur les plaintes utilisateurs des plateformes existantes (SeLoger, LeBonCoin, Bien'ici, Logic-Immo, PAP) et les problèmes structurels du marché français.

### 11.1 Données fragmentées

**Pain point** : L'utilisateur doit consulter 5+ sources (cadastre, DVF, Géorisques, DPE, loyers, PLU) pour avoir une vision complète d'un bien. Aucune plateforme ne les agrège.

**Idées d'adressage** :
- Couche de données unifiée : croiser cadastre + DVF + Géorisques + DPE + taxe en une seule vue par parcelle/bien
- Score composite qui intègre toutes les dimensions (prix, risque, énergie, fiscalité)
- API backend qui fait le croisement, frontend qui affiche la synthèse

### 11.2 Géolocalisation fausse

**Pain point** : Sur Bien'ici et Logic-Immo, les biens sont affichés jusqu'à 50km de leur position réelle. Les pins sont mal placés.

**Idées d'adressage** :
- Utiliser la géométrie cadastre (polygons) plutôt que les coordonnées déclarées par l'agent
- Cross-géocodage : vérifier l'adresse contre l'API IGN
- Afficher une incertitude de localisation (zone de flou) plutôt qu'un point faux

### 11.3 Annonces obsolètes / vendues

**Pain point** : Biens déjà vendus restent affichés. Les agents republient pour rester visibles. 40-60% de doublons entre plateformes.

**Idées d'adressage** :
- Croiser avec les transactions DVF récentes pour détecter les biens vendus
- Indicateur "jours en ligne" + baisse de prix = signal d'urgence ou d'erreur
- Scoring de fraîcheur de l'annonce (dernière mise à jour, cohérence des données)
- Pas d'annonce legs si pas de source fiable

### 11.4 DPE non fiable

**Pain point** : 71% des DPE ne reflètent pas la conso réelle. Un même bien peut avoir 2 classes d'écart selon le diagnostiqueur. La réforme 2026 reclassifie 850k logements par un changement de formule.

**Idées d'adressage** :
- Afficher le DPE mais avec un indice de fiabilité (nombre de DPE du diagnostiqueur, ancienneté)
- Croiser avec les données de conso réelle si disponibles (hub EDF/Enedis)
- Montrer l'impact financier : "Si le DPE est F, interdiction de louer à horizon 2034, perte de valeur estimée -18%"
- Ne pas utiliser le DPE comme critère binaire mais comme indicateur pondéré

### 11.5 Pas de comparateur natif

**Pain point** : Aucune plateforme FR n'offre de comparaison side-by-side. Les utilisateurs utilisent des outils tiers (Pierro, BienCheck, Aquiz).

**Idées d'adressage** :
- Comparateur intégré : sélectionner 2-4 biens, vue côte à côte
- Métriques normalisées : prix/m², DPE, risques, loyer estimé, taxe foncière
- Score composite comparatif : "A est meilleur que B sur 6/8 critères"
- Export PDF du comparatif

### 11.6 Alertes spam / pas de contrôle

**Pain point** : SeLoger et Logic-Immo envoient trop d'alertes. Pas de contrôle de fréquence. Doublons entre plateformes. PAP limite à 10 alertes.

**Idées d'adressage** :
- Contrôle de fréquence : quotidien, hebdo, instantané
- Dédoublonnage : même bien sur plusieurs sources = une seule alerte
- Filtre "nouveau uniquement" : masquer les biens déjà vus
- Resume hebdomadaire : "5 nouveaux biens correspondent à votre projet X"

### 11.7 Analyse financière déconnectée

**Pain point** : Les simulateurs de crédit sont des outils séparés. Pas de "puis-je me le permettre?" sur la fiche bien. Les simulateurs omettent assurance, frais notaire, garantie.

**Idées d'adressage** :
- Simulateur inline sur chaque fiche : mensualité estimée pour ce bien
- Calcul incluant : assurance, notaire (7-8% ancien / 2-3% neuf), garantie
- Indicateur de rentabilité pour investissement : cashflow mensuel, TRI
- Comparer le coût total sur 5/10/20 ans

### 11.8 PLU illisible

**Pain point** : 35k documents locaux, chaque commune a ses règles. La méconnaissance du PLU est la 1ère cause de refus de permis.

**Idées d'adressage** :
- Interprétation simplifiée : "Constructible Oui/Non" avec raison
- Règles clés extraites : hauteur max, COS, CUS, recul, matériaux
- Alertes : "Attention : ce terrain est en zone AU, constructibilité conditionnée à un PLU futur"
- Lien direct vers le règlement PDF

### 11.9 Risques naturels bruts

**Pain point** : Géorisques agrège 30+ bases sans hiérarchisation. L'ERP est une liste administrative, pas une aide à la décision.

**Idées d'adressage** :
- Synthèse hiérarchisée : "Risque principal : argiles (élevé). Risque secondaire : inondation (moyen). Pas de risque sismique."
- Score de risque composite (0-100)
- Impact financier estimé : "Prime d'assurance +X€/an en zone inondable"
- Carte des risques superposée à la parcelle

### 11.10 Foncière opaque

**Pain point** : +37% en 10 ans. Base de calcul data de 1974. Varie énormément d'une commune à l'autre. Non visible avant l'achat.

**Idées d'adressage** :
- Taxe foncière estimée par commune (données REI)
- Afficher la tendance : "+X% sur 5 ans"
- Comparer avec les communes voisines
- Intégrer dans le calcul de rentabilité (investissement)

### 11.11 Comparaison de communes difficile

**Pain point** : DVF avec décalage publication, peu de transactions en rural, sources qui se contredisent (tension locative LocService vs Bien'ici).

**Idées d'adressage** :
- Fiche commune : synthèse DVF + risques + DPE + loyers + fiscalité
- Indicateur de fiabilité : "Prix basé sur 45 transactions (fiabilité moyenne)" vs "2 transactions (fiabilité faible)"
- Normaliser les sources conflictuelles avec un score de confiance

---

## 17. MVP (v0.1)

Le MVP se concentre sur **logement principal — terrain enterrée** + **système de projets** :

1. **Backend** :
   - API FastAPI avec CRUD projets
   - Pipeline ETL cadastre → table `terrains` (réplication locale — 27.9)
   - Pipeline ETL altimétrie (pente, exposition → colonnes dédiées)
   - Scoring terrain enterrée (pente, prix, constructibilité)
   - Détection nouvelles offres
   - PostgreSQL + PostGIS + Martin (tuiles)

2. **Frontend** :
   - Page d'accueil : liste projets + création
   - Wizard création projet (étapes + progress bar)
   - Carte MapLibre avec parcelles
   - Recherche par adresse
   - Filtres (surface, prix, pente, zone)
   - Fiche terrain détaillée
   - Score visuel

3. **hors scope MVP** :
   - Autres catégories (terrain classique, maison, appt)
   - Mode investissement (calques, dessin zone)
   - Auth / comptes users
   - Comparateur
   - Export PDF

---

## 18. Commandes utiles

```bash
# Backend (python/)
cd python
uv sync
uv run uvicorn app.main:app --reload
uv run pytest

# Frontend (typescript/)
cd typescript
pnpm install
pnpm dev
pnpm build

# Racine (gate complet)
make ci
```

---

## 19. Prochaines étapes

1. [ ] Setup backend FastAPI + PostGIS + Martin
2. [ ] Modèle de données projets + terrains
3. [ ] API CRUD projets
4. [ ] Pipeline ETL cadastre (Airflow + dbt → table `terrains`)
5. [ ] Pipeline ETL altimétrie (pente, exposition)
6. [ ] Implémenter scoring terrain enterrée
7. [ ] Setup frontend SvelteKit
8. [ ] Page d'accueil (liste projets)
9. [ ] Wizard création projet
10. [ ] Carte MapLibre + overlay parcelles
11. [ ] Connecter frontend ↔ backend
12. [ ] Détection nouvelles offres
