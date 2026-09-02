# Wave 08 — Backoffice / Admin

> Interface d'administration pour gérer les utilisateurs, annonces, signalements et feedbacks.

> Retour au [spec principal](../README.md)

---

## 29. Backoffice

### Accès

- Route `/admin` (protégée, rôle admin requis)
- Authentification renforcée (2FA obligatoire pour les admins)
- Log de toutes les actions admin

### Rôles

| Rôle | Permissions |
|---|---|
| **User** | Accès standard |
| **Moderator** | Gérer reports, modérer listings |
| **Admin** | Tout + gérer users + config |

> Rôles stockés dans la colonne `users.role` — modèle wave-01 §13.

### Navigation

```
┌─────────────────────────────────────────────────────┐
│  🛡️ Plot Admin                                      │
├──────────┬──────────────────────────────────────────┤
│          │                                          │
│ 📊 Dash  │  Contenu principal                       │
│ 👥 Users │                                          │
│ 📋 Annonc│                                          │
│ 🚩 Signa │                                          │
│ 💬 Feedb │                                          │
│ ⚙️ Config│                                          │
│          │                                          │
└──────────┴──────────────────────────────────────────┘
```

---

## 30. Dashboard

### Métriques

| Métrique | Description |
|---|---|
| Utilisateurs | Total, actifs (7j/30j), nouveaux (sem.) |
| Annonces | Total, actives, vendues/louées, supprimées |
| Signalements | En attente, traités, taux de validation |
| Feedbacks | Nouveaux, par type (bug/idée/question) |
| Projets | Total, créés cette semaine |
| Revenus | Si monétisation future |

### Graphiques

- Courbe utilisateurs (inscription/jour)
- Courbe annonces (dépôt/jour)
- Top 10 communes (annonces)
- Répartition par type (terrain/maison/appt)

---

## 31. Gestion utilisateurs

### Liste des users

| Colonne | Description |
|---|---|
| Avatar | Photo |
| Nom / Email | Identité |
| Type | individual / agency / notary |
| Score fiabilité | 0-100 |
| Annonces | Nombre |
| Inscrit le | Date |
| Actions | Voir / Bloquer / Supprimer |

### Fiche user

| Section | Contenu |
|---|---|
| Profil | Infos complètes, type, SIRET |
| Annonces | Liste des annonces avec statuts |
| Signalements | Signalements reçus et envoyés |
| Score fiabilité | Détail du calcul |
| Activité | Historique (connexions, actions) |

### Actions admin

| Action | Description |
|---|---|
| **Bloquer** | Bloquer le compte pour modération (récupérable) — colonne `users.is_blocked` : masque les contenus mais **n'empêche pas le login** ; la désactivation complète passe par `is_active` |
| **Supprimer** | Suppression définitive admin (hard delete — distinct de la suppression propriétaire qui reste récupérable 30 j) + données |
| **Changer le rôle** | User ↔ Moderator ↔ Admin |
| **Reset score** | Remettre le score de fiabilité à 50 |
| **Vérifier** | Marquer email comme vérifié manuellement |

---

## 32. Modération annonces

### Liste des annonces à modérer

| Filtre | Description |
|---|---|
| Statut | active / under_offer / sold / reported |
| Type | terrain / house / apartment |
| Source | manual / import / claim (enum canonique wave-01) |
| Date | Période |
| Signalée | Oui / Non |

### Actions de modération

| Action | Description |
|---|---|
| **Approuver** | Valider l'annonce |
| **Rejeter** | Refuser avec motif |
| **Modifier** | Corriger les données |
| **Suspendre** | Masquer temporairement |
| **Supprimer** | Suppression définitive admin (hard delete — distinct de la suppression propriétaire, récupérable 30 j) |

---

## 33. Gestion signalements

### Liste des signalements

| Colonne | Description |
|---|---|
| Annonce | Bien signalé |
| Signalé par | Utilisateur (anonyme si déconnecté) |
| Raison | dropdown (sold, under_offer, fraud, price_error, other) |
| Date | Quand |
| Statut | pending / processed / rejected |
| Actions | Traiter / Rejeter |

### Actions

| Action | Description |
|---|---|
| **Traiter** | Valide → archiver/supprimer l'annonce |
| **Rejeter** | Non validé → garder l'annonce |
| **Contacter** | Email au propriétaire de l'annonce |
| **Bloquer** | Si signalements abusifs (anti-abus signaleur : à spécifier dans wave-12 — 27.25) |

---

## 34. Gestion feedbacks

### Liste des feedbacks

| Colonne | Description |
|---|---|
| Type | 🐛 bug / 💡 idea / ❓ question / 😤 complaint |
| Message | Contenu tronqué |
| Page | Page courante |
| Utilisateur | Si connecté |
| Date | Quand |
| Statut | new / in_progress / processed / archived (enum canonique wave-01) |
| Actions | Répondre / Résoudre / Fermer |

### Actions

| Action | Description |
|---|---|
| **Répondre** | Email de réponse à l'utilisateur |
| **Résoudre** | Marquer comme résolu |
| **Fermer** | Fermer sans réponse |
| **Convertir en issue** | Créer un ticket GitHub |
