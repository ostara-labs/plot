# Wave 12 — Modération & anti-abus

> Décision 27.25 (maturation wave-01) : **analyse préalable obligatoire** avant toute spécification.

## Contexte

L'escalade automatique des signalements (wave-05 : archivage à 3+, suppression à 5+) et les actions de modération (wave-08 : Traiter/Rejeter/Contacter/Bloquer) coexistent sans interaction définie. Par ailleurs, **aucun mécanisme ne punit les signaleurs malveillants** (faux signalements répétés contre un annonceur honnête). Cette wave traite les deux, mais **après une phase d'analyse**.

## ⚠️ Phase 1 — Analyse préalable (bloquante)

Questions à instruire avant d'écrire la spec :

1. **Volume** : combien de signalements attendus (ratio annonces × utilisateurs) ? Viable de tout envoyer en file manuelle ?
2. **Seuils** : les seuils actuels (1 badge / 2 notification / 3+ archivage / 5+ suppression) sont-ils robustes au gaming (bombardement coordonné) ?
3. **Signalement abusif** : définition opérationnelle (taux de rejet ? motifs répétés ?) et preuve (comment distinguer abus vs erreur de bonne foi ?)
4. **Score signaleur** : formule, pénalités, seuil de blocage, recours possible ?
5. **RGPD** : les pénalités signaleur sont des décisions automatisées — quel encadrement (art. 22) ?
6. **Charge modération** : qui modère à quel moment ? File unifiée (tout signalement) vs file exceptions (Faux/arnaque + réactivations) — arbitrée par les données du point 1.
7. **Handoff auto ↔ manuel** : quid des compteurs quand le modérateur rejette un signal ? Restauration d'annonce auto-archivée ?

## Périmètre pressenti (phase 2 — spécification)

- File de modération (unifiée ou exceptions — selon analyse)
- Interaction escalade automatique ↔ actions manuelles (reset compteurs, restauration)
- Anti-abus signaleur : score, pénalités, blocage, recours
- Analytics modération (volume, délais de traitement, faux positifs)

## Liens

- wave-01 : `reports.status` (pending/processed/rejected), `users.is_blocked`, 27.25
- wave-05 : escalade automatique, score de fiabilité
- wave-08 : backoffice, modération annonces/signalements
- wave-03 : claims (vérification manuelle « ou auto si possible » — même famille de questions)

## Statut

🔬 **Analyse préalable à mener avant toute spécification** — ne pas implémenter avant validation de la phase 1.
