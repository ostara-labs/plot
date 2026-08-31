# Wave 11 — Espace annonceur

> Décision 27.23 (maturation wave-01) : dashboard annonceur **complet**.

## Contexte

wave-03 (contact vendeur) référence un « dashboard » du vendeur et wave-05 rend le score de fiabilité « visible sur le profil du propriétaire » — mais aucun espace annonceur n'était spécifié (wave-08 = backoffice admin, pas annonceur). Cette wave comble le trou : c'est l'espace où l'annonceur gère ses annonces, ses contacts et suit sa réputation.

## Périmètre pressenti

| Bloc | Contenu |
|---|---|
| **Mes annonces** | Liste (statut, dates, nombre de vues, signalements), actions rapides (modifier, marquer vendu/loué, désactiver, supprimer), relance « annonce à mettre à jour » |
| **Boîte de contacts** | Historique des contacts (table `contacts` — wave-01 §13), réponse inline, statut lu/non-lu, taux de réponse |
| **Stats** | Vues de fiche, contacts reçus, délai moyen de réponse, évolution |
| **Score de fiabilité** | Score visible (wave-05), détail des facteurs, historique |

## Règle fiabilité liée au contact (27.23)

**+1/mois si taux de réponse > 80 % sous 72 h** (donnée : table `contacts` + réponses). S'intègre aux facteurs wave-05.

## Liens

- wave-01 : modèle (`contacts`, `users.score_fiabilite`, 27.23)
- wave-03 : dépôt d'annonce, contact vendeur
- wave-05 : score de fiabilité
- wave-07 : notifications annonceur (signalement, contact, réponse)

## Statut

🔜 À spécifier — murir via la checklist 8 critères avant implémentation. UX : wireframe du dashboard à valider avant frontend (règle 27.18).
