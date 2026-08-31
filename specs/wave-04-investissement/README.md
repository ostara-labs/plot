# Wave 04 — Investissement

> Carte investissement : calques interactifs, outils de dessin de zone, zones de priorité et pondération des critères.

> Retour au [spec principal](../README.md)

---

## 7. Carte — Investissement

### Layout

```
┌──────────────────────────────────────────────┐
│  [Calques ▼] [Outils dessin ▼]    [Filtres]  │
├──────────────────────────────────────────────┤
│                                              │
│              CARTE MAPLIBRE                  │
│           (calques interactifs)              │
│                                              │
│    ┌─────────────────────────────────┐       │
│    │ Zone dessinée (polygone)        │       │
│    └─────────────────────────────────┘       │
│                                              │
├──────────────────────────────────────────────┤
│  Sidebar résultats (liste biens dans zone)   │
└──────────────────────────────────────────────┘
```

### Calques (toggle)

| Calque | Rendu | Source |
|---|---|---|
| 💰 Rentabilité brute | Heatmap rouge/vert | DVF + loyers |
| 📈 Prix / m² | Heatmap bleu/orange | DVF |
| 🏠 Loyer / m² | Heatmap vert/jaune | OLL |
| 🚇 Transport en commun | Isochrone 15/30/45 min | IGN |
| ⚠️ Risques naturels | Overlay vert/jaune/rouge | Géorisques |
| 🌡️ DPE | Points colorés A-G | ADEME |

> **Sources (27.9)** : toutes les données des calques proviennent des tables locales (réplication ETL Airflow + dbt). Rendu carto via tile server Martin (27.5).

Plusieurs calques actifs simultanément avec opacité adjustable.

### Outils de dessin

| Outil | Description |
|---|---|
| 🖊️ Polygone libre | Dessiner une zone arbitraire |
| ⬜ Rectangle | Dessiner un rectangle |
| ⭕ Cercle | Centre + rayon |
| 🧹 Gomme | Dessiner pour retirer de la zone (soustraction) |
| 🗑️ Reset | Effacer toutes les zones dessinées |

La zone dessinée devient le périmètre de recherche. Les résultats se mettent à jour en temps réel. La zone est sauvegardée dans le projet.

### Zones de priorité

L'utilisateur peut dessiner plusieurs zones avec des niveaux de priorité différents. Les biens dans les zones prioritaires sont mis en avant visuellement.

| Priorité | Couleur | Usage |
|---|---|---|
| 🔴 Haute | Rouge | Zone idéale, je cherche ici en priorité |
| 🟠 Moyenne | Orange | Zone intéressante, à considérer |
| 🟢 Basse | Vert | Zone de repli, si rien d'autre |

Stockage : table `zones_priorite` (modèle wave-01 §13).

**Exemple** : Je veux acheter dans Lyon 3e en priorité (rouge), mais Lyon 6e et 7e sont acceptables (orange). Villeurbanne c'est OK si le prix est intéressant (vert).

Les biens dans les zones prioritaires sont :
- Mis en avant dans la liste (tri par priorité + score)
- Affichés en surbrillance sur la carte
- Le scoring peut prendre en compte la zone de priorité comme critère bonus

### Pondération des critères

L'utilisateur peut ajuster les poids de chaque critère en temps réel via des sliders. Les scores se recalculent à chaud sur les colonnes pré-calculées (27.2) avec cache Redis (27.14) — latence cible < 100 ms.

```
┌─────────────────────────────────────────┐
│  Pondération des critères               │
├─────────────────────────────────────────┤
│  Prix / m²          ████████░░  40%     │
│  Surface            ██████░░░░  30%     │
│  Transport          ████░░░░░░  20%     │
│  DPE                ██░░░░░░░░  10%     │
├─────────────────────────────────────────┤
│  [Réinitialiser]   [Appliquer]          │
└─────────────────────────────────────────┘
```

Le total des poids doit toujours valoir 100%. Quand l'utilisateur modifie un slider, les autres s'adaptent automatiquement.

**Fonctionnalités** :
- Sliders interactifs avec pourcentage affiché
- Réinitialiser aux poids par défaut
- Sauvegarder des profils de pondération personnalisés
- Stockage : table `profils_ponderation` (modèle wave-01 §13).
- Aperçu en temps réel sur la carte (les scores changent quand on bouge les sliders)
