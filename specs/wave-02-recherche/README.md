# Wave 02 — Recherche

> Recherche de logement principal : page d'accueil, wizard de création de projet, carte logement et critères d'évaluation par catégorie.

> Retour au [spec principal](../README.md)

---

## 4. Page d'accueil — Mes projets

La page `/` affiche la liste des projets existants, permet d'en créer un nouveau, et d'**ajouter une annonce**.

### Liste des projets

```
┌─────────────────────────────────────────────────────┐
│  🏠 Terrain enterrée Aude              12 nouvelles │
│     Critères : pente < 15%, expos. sud, < 200k€     │
│     [Charger]  [Dupliquer]  [Modifier]  [Supprimer] │
├─────────────────────────────────────────────────────┤
│  🏠 Maison Colmar                      3 nouvelles  │
│     Critères : 3ch, DPE A-C, > 80m², < 350k€       │
│     [Charger]  [Dupliquer]  [Modifier]  [Supprimer] │
├─────────────────────────────────────────────────────┤
│  💰 Invest appt Lyon 3e                7 nouvelles  │
│     Critères : rentab. > 6%, 2-3ch, proche métro    │
│     [Charger]  [Dupliquer]  [Modifier]  [Supprimer] │
└─────────────────────────────────────────────────────┘

[+ Nouveau projet]
```

### Actions projet

| Action | Description |
|---|---|
| **Charger** | Ouvre la carte avec les critères et résultats du projet |
| **Dupliquer** | Copie le projet avec un nom modifiable |
| **Modifier** | Change les critères, recalcule les résultats |
| **Supprimer** | Archive le projet |

### Indicateur de nouvelles offres

Badge vert avec le nombre de nouveaux résultats depuis la dernière consultation. Calculé en comparant les résultats actuels avec ceux sauvegardés.

### Boutons d'action

```
[+ Nouveau projet]   [+ Déposer une annonce]
```

---

## 5. Création de projet — Wizard

Le bouton "+ Nouveau projet" lance un wizard par étapes avec témoin de progression.

### Étapes

```
[1] Type ─────── [2] Catégorie ─────── [3] Zone ─────── [4] Critères ─────── [5] Budget
   ●                  ○                    ○                  ○                   ○
```

#### Étape 1 : Type de projet

| Choix | Description |
|---|---|
| 🏠 **Logement principal** | Je cherche un logement pour y vivre |
| 💰 **Investissement** | Je cherche un bien locatif |

#### Étape 2 : Catégorie

Selon le type choisi :

**Logement principal :**
| Catégorie | Description |
|---|---|
| Terrain maison enterrée | Terrain pour construction enterrée/semi-enterrée |
| Terrain construction classique | Terrain pour maison traditionnelle |
| Maison | Maison existante |
| Appartement | Appartement existant |

**Investissement :**
| Catégorie | Description |
|---|---|
| Maison | Maison en location |
| Appartement | Appartement en location |
| Terrain | Terrain à construire puis louer |

#### Étape 3 : Zone géographique

- Recherche par adresse / ville
- Ou dessin de zone sur la carte (polygone, rectangle, cercle)
- Rayon de recherche configurable

#### Étape 4 : Critères (selon catégorie)

Chaque catégorie a ses propres critères avec sliders et toggle :

**Terrain enterrée :**
| Critère | Widget | Défaut |
|---|---|---|
| Pente max | Slider 0-45% | 15% |
| Exposition | Toggle (S, SW, W, SE, E, NE, N, NW) | S, SW, SE |
| Surface min | Slider 200-5000 m² | 500 m² |
| Zone | Toggle (urbain, périurbain, rural) | périurbain |
| Constructible | Toggle | Oui |
| Distance ville max | Slider 5-100 km | 30 km |

**Terrain classique :**
| Critère | Widget | Défaut |
|---|---|---|
| Surface min | Slider 200-5000 m² | 500 m² |
| Zone | Toggle | périurbain |
| Constructible | Toggle | Oui |

**Maison :**
| Critère | Widget | Défaut |
|---|---|---|
| Chambres min | Slider 1-6 | 2 |
| Surface min | Slider 20-300 m² | 60 m² |
| DPE max | Toggle (A-G) | C |
| Jardin | Toggle | Non |

**Appartement :**
| Critère | Widget | Défaut |
|---|---|---|
| Chambres min | Slider 1-6 | 1 |
| Surface min | Slider 10-200 m² | 30 m² |
| DPE max | Toggle (A-G) | C |
| Étage min/max | Double slider | 1-5 |

**Investissement (toutes catégories) :**
| Critère | Widget | Défaut |
|---|---|---|
| Rentabilité min | Slider 0-15% | 5% |
| Loyer min | Slider 200-3000 € | 500 € |

#### Étape 5 : Budget

- Budget maximum (slider ou input)
- Affiche le nombre estimé de résultats

#### Récapitulatif

Avant sauvegarde, récap visuel de tous les critères avec option de modification.

---

## 6. Carte — Logement principal

### Layout

```
┌──────────────────────────────────────────────┐
│  [Adresse] [🔍]                    [Filtres] │
├────────────────────┬─────────────────────────┤
│                    │                         │
│                    │    CARTE MAPLIBRE       │
│   Filtres latéraux │    (parcelles/biens)    │
│                    │                         │
│                    │                         │
├────────────────────┤                         │
│   Résultats        │                         │
│   (liste scroll)   │                         │
└────────────────────┴─────────────────────────┘
```

### Filtres contextuels

Les filtres affichés dépendent de la catégorie du projet. L'utilisateur peut affiner sans modifier le projet.

### Overlay carte

- **Parcelles/biens** : markers ou polygons colorés par score
- **Clusterisation** : quand beaucoup de résultats
- **Clic** : popup résumé + lien fiche détaillée
- **Heatmap** : optionnel, scoring visuel

---

## 10. Critères d'évaluation par catégorie

### 9.1 Terrain maison enterrée

| Critère | Poids | Source |
|---|---|---|
| Pente | 25% | IGN Altimétrie |
| Exposition | 20% | Calcul géométrie |
| Prix / m² | 20% | DVF |
| Distance grandes villes | 15% | Géocodage IGN |
| Constructibilité | 10% | PLU / GPU |
| Risques naturels | 10% | Géorisques |

### 9.2 Terrain construction classique

| Critère | Poids | Source |
|---|---|---|
| Surface | 25% | Cadastre |
| Prix / m² | 25% | DVF |
| Constructibilité | 20% | PLU / GPU |
| Accessibilité route | 15% | IGN / OSM |
| Proximité POI | 10% | OSM |
| Risques naturels | 5% | Géorisques |

### 9.3 Maison existante

| Critère | Poids | Source |
|---|---|---|
| Prix / m² | 25% | DVF |
| DPE | 20% | ADEME |
| Surface habitation | 20% | Annonce / DVF |
| Transport en commun | 15% | IGN / OSM |
| Risques naturels | 10% | Géorisques |
| Proximité POI | 10% | OSM |

### 9.4 Appartement

| Critère | Poids | Source |
|---|---|---|
| Prix / m² | 25% | DVF |
| DPE | 20% | ADEME |
| Transport en commun | 20% | IGN / OSM |
| Surface | 15% | Annonce / DVF |
| Étage / ascenseur | 10% | Annonce |
| Risques naturels | 10% | Géorisques |

### 9.5 Investissement locatif

| Critère | Poids | Source |
|---|---|---|
| Rentabilité brute | 30% | DVF + loyers |
| Prix / m² | 20% | DVF |
| Demande locative | 20% | OLL / INSEE |
| Transport en commun | 15% | IGN / OSM |
| Risques naturels | 10% | Géorisques |
| DPE | 5% | ADEME |

Les poids sont personnalisables par l'utilisateur.

### 9.6 Critères transverses — risques technologiques, climat & environnement

Ces critères s'appliquent à **toutes les catégories** (logement et investissement). Ils sont ajoutés aux grilles ci-dessus, avec leurs propres pondérations par défaut et toggles pour les désactiver.

| Critère | Défaut | Source |
|---|---|---|
| Distance site nucléaire (INB) | > 10 km | Géorisques V2 `/installations_nucleaires` |
| Distance site SEVESO (seuil haut) | > 1 km | Géorisques V2 `/installations_classees?statutSeveso=SEUIL_HAUT` |
| Distance ICPE (hors SEVESO) | > 300 m | Géorisques V2 `/installations_classees` |
| Sols pollués (SIS/BASOL/CASIAS) | Aucun dans 200 m | Géorisques V2 `/ssp` |
| Anciennes mines / carrières souterraines | Aucune dans 200 m | Géorisques V2 `/cavites` |
| Distance ligne haute tension (63-400 kV) | > 200 m | ODRÉ (RTE) lignes aériennes/souterraines |
| Risque feux de forêt | Toggle (exclure les zones à risque) | Géorisques V1 `risques` (FEUFORET) + BDIFF |
| Submersion marine / érosion côtière | Toggle (exclure zones PPRL + communes RTC) | Géorisques V1 `azi`/`ppr` + GéoLittoral |
| Climat futur (canicule, sécheresse) | Jours très chauds / sols secs à 2050 max | Climadiag Commune / DRIAS-2020 |
| Climat actuel (temp, ensoleillement) | Normales 1991-2020 | Météo-France |
| Protection patrimoine (MH, sites, UNESCO, Natura 2000) | Badge info + avis ABF si périmètre MH | Géoplateforme WFS + data.culture.gouv.fr |
| Zones humides / ZNIEFF | Badge info (contrainte procédurale) | Géoplateforme WFS |
| Plan d'exposition au bruit (aérodrome) | Aucun logement en zone A/B | Géoplateforme WFS `dgac_peb_arrete_wfs` |
| Bruit routes/rails | Classe Lden max (3 zones considérées acceptables) | Cerema CBS |
| Qualité de l'air | Indice ATMO moyen max | Atmo Data |
| Antennes relais | Comptage dans 300 m (info) | ANFR |
| Fibre optique | Ou / Non / En cours de déploiement | ARCEP Ma connexion internet |
| Eau potable au réseau | Oui/Non | SISPEA |
| Assainissement collectif | Oui/Non (sinon SPANC/ANC) | SISPEA |
| Couverture mobile 4G | Oui/Non | ARCEP Mon réseau mobile |

**Règles de scoring transverses** :
- Les critères de risque technologique (nucléaire, SEVESO) sont des **toggles d'exclusion** plus que des critères pondérés : en dessous des seuils, le bien est écarté (ou fortement pénalisé, configurable).
- Les protections patrimoine/environnement sont des **badges info** dans la fiche bien (avec lien vers le service officiel) et n'affectent pas le score par défaut — sauf EBC / PEB A-B / sites classés qui sont des **exclusions dures** (non constructibles).
- Les critères "confort" (fibre, bruit, air, antennes) sont pondérés dans le score avec des poids faibles par défaut.
- Le **climat futur** est un critère de tri pertinent pour l'achat d'un logement qu'on gardera 20+ ans : intégré aux grilles avec poids modéré (3-5%) suivant la catégorie.

---

## 11. Favoris & sélections

### Fonctionnalité

L'utilisateur peut sauvegarder des biens en favoris sans les associer à un projet.

### Actions

| Action | Description |
|---|---|
| **Ajouter aux favoris** | Clic sur le cœur (connecté) ou stocké localement (déconnecté) |
| **Retirer des favoris** | Clic sur le cœur barré |
| **Voir les favoris** | Page dédiée `/favoris` avec liste et carte |
| **Déplacer vers projet** | Associer un favori à un projet existant |

### Données

| Champ | Type | Description |
|---|---|---|
| user_id | UUID | Utilisateur (null si déconnecté) |
| bien_id | UUID | Bien favori |
| projet_id | UUID | Projet associé (optionnel) |
| created_at | TIMESTAMPTZ | Date d'ajout |
| notes | TEXT | Note personnelle (optionnel) |

---

## 12. Export PDF

### Contenu du PDF

| Section | Contenu |
|---|---|
| En-tête | Logo Plot, date, nom du projet |
| Critères | Résumé des critères de recherche |
| Liste résultats | Top 10 biens avec score, prix, adresse |
| Fiche bien (si sélection) | Détails complets d'un bien |
| Carte | Capture de la carte avec les biens |
| Comparatif (si sélection) | Tableau comparatif side-by-side |

### Format

- A4 portrait
- Basé sur les données du projet
- Template responsive (s'adapte au contenu)
- Généré côté serveur (FastAPI + WeasyPrint ou ReportLab)

---

## 13. Partage

### Types de partage

| Type | Description | URL |
|---|---|---|
| **Projet** | Partager les critères + résultats | `/partage/projet/[token]` |
| **Annonce** | Partager une fiche bien | `/annonce/[id]` |
| **Comparatif** | Partager une sélection de biens | `/partage/compare/[token]` |
| **Carte** | Partager une vue carte avec filtres | `/partage/carte/[token]` |

### Mécanique

- Génère un lien unique (token)
- Le destinataire voit une version read-only
- Pas besoin de compte pour consulter
- Le lien expire après 30 jours (configurable)
- Le créateur peut révoquer le lien
