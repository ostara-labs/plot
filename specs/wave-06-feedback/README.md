# Wave 06 — Feedback

> Feedback in-app : widget de remontée des doléances, idées, questions et problèmes depuis toutes les pages.

> Retour au [spec principal](../README.md)

---

## 16. Feedback in-app

Un widget de feedback accessible depuis toutes les pages permet aux utilisateurs de remonter leurs doléances, idées, questions et problèmes.

### Fonctionnalités

| Fonction | Description |
|---|---|
| **Bulle flottante** | Icône discrète en bas à droite, always visible |
| **Catégorisation** | Bug, Idée, Question, Doléance |
| **Contexte auto** | Page courante, projet chargé, filtres actifs |
| **Capture d'écran** | Optionnel : screenshot de la page courante |
| **Suivi de statut** | L'utilisateur voit si son feedback est traité |
| **Réponse** | L'équipe peut répondre (notification email optionnelle) |

### UX

```
┌─────────────────────────────┐
│  💬 Votre retour            │
├─────────────────────────────┤
│  Type : [Bug ▼]             │
│                             │
│  [Votre message...]         │
│                             │
│  📎 Joindre un screenshot   │
│                             │
│  Page : /logement/buried-   │
│  terrain (auto-détecté)     │
│                             │
│  [Envoyer]                  │
└─────────────────────────────┘
```
