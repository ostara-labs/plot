# Wave 09 — PWA / Offline

> Progressive Web App : installation, mode hors-ligne, cache intelligent et synchronisation.

> Retour au [spec principal](../README.md)

---

## 35. Progressive Web App (PWA)

### Objectif

Plot fonctionne comme une application native sur mobile/tablette tout en restant une app web. L'utilisateur peut installer Plot sur son écran d'accueil et l'utiliser hors-ligne.

### Manifest

```json
{
  "name": "Plot — Trouvez le meilleur logement",
  "short_name": "Plot",
  "description": "Outil de recherche immobilière basé sur les données ouvertes",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0f172a",
  "theme_color": "#3b82f6",
  "orientation": "any",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

### Installation

| Étape | Description |
|---|---|
| 1 | Bannière "Ajouter à l'écran d'accueil" (afterinstallprompt) |
| 2 | Confirmation native du navigateur |
| 3 | Icône sur l'écran d'accueil |
| 4 | Lancement en mode standalone (pas de barre d'adresse) |

---

## 36. Service Worker

### Stratégie de cache

| Ressource | Stratégie | TTL |
|---|---|---|
| HTML (pages statiques) | Network First | Fallback cache 7j |
| CSS / JS | Stale While Revalidate | Cache 30j |
| Fonts | Cache First | Cache 1 an |
| Images (non-carte) | Cache First | Cache 30j |
| Tiles MapLibre | Cache First + Network | Cache 14j (quota 500Mo) |
| API calls | Network Only | — |
| Données projet (offline) | Cache + Sync | Jusqu'à sync |

### Lifecycle

```
Install → Activate → Fetch (intercept)
    ↓         ↓            ↓
  Cache    Claim    Cache/Network决策
```

### Offline fallback

| État réseau | Comportement |
|---|---|
| En ligne | Fonctionnement normal |
| Hors-ligne | Pages statiques depuis le cache, tiles carte depuis le cache, données projets depuis localStorage |
| Rétabli | Sync automatique des données en attente |

---

## 37. Données hors-ligne

### Ce qui fonctionne hors-ligne

| Fonctionnalité | Mode offline |
|---|---|
| Consulter les projets enregistrés | ✅ Depuis localStorage |
| Voir les résultats dernière consultation | ✅ Depuis le cache |
| Naviguer sur la carte (déjà chargée) | ✅ Tiles en cache |
| Ajouter des favoris | ✅ Sync différée |
| Signaler une annonce | ✅ Sync différée |
| Créer un projet | ⚠️ Stocké localement, sync à la reconnexion |

### Ce qui ne fonctionne PAS hors-ligne

| Fonctionnalité | Raison |
|---|---|
| Nouvelle recherche | Données serveur nécessaires |
| Déposer une annonce | Upload impossible |
| Contacter un vendeur | Envoi impossible |
| Voir le score mis à jour | Calcul serveur |

### Sync différée

| Opération | File d'attente | Priorité |
|---|---|---|
| Favori ajouté | `sync_favoris` | Haute |
| Signalement | `sync_signalements` | Haute |
| Projet créé | `sync_projets` | Moyenne |
| Feedback | `sync_feedback` | Basse |

Le service worker tente la sync à chaque retour en ligne. Si échec, réessaie avec backoff exponentiel.

---

## 38. Cache des tiles carte

### Stratégie

Les tiles MapLibre GL JS sont volumineuses. Stratégie de cache agressive :

| Zone | TTL | Taille max |
|---|---|---|
| Zone viewport (viewport courant) | 14 jours | 200 Mo |
| Zone projet (rayon de recherche) | 14 jours | 300 Mo |
| Tiles hors zone | Pas de cache | — |

### Nettoyage

- Quota max : 500 Mo pour les tiles
- LRU (Least Recently Used) pour libérer de l'espace
- Nettoyage automatique des tiles > 14 jours

### Préchargement

- Précharger les tiles autour de la position courante
- Précharger les tiles du périmètre du projet actif
- Stratégie : 2 zoom levels autour du zoom courant
