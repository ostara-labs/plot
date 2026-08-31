# Wave 05 — Confiance

> Signalement par les utilisateurs et score de fiabilité des annonceurs. Ces mécanismes sont issus de la section "Déposer une annonce" du spec, dont le reste est traité dans la [Wave 03 — Annonces](../wave-03-annonces/README.md).

> Retour au [spec principal](../README.md)

---

## Signalement par les utilisateurs

Un utilisateur (y compris déconnecté) peut signaler une annonce comme :

| Signal | Conséquence |
|---|---|
| **Vendu** | Propriétaire notifié, annonce marquée "vendu" si confirmé |
| **Sous offre** | Propriétaire notifié, badge "sous offre" |
| **Faux / arnaque** | Vérification manuelle, annonce passe en statut `signalée` (enum wave-01) |
| **Erreur de prix** | Propriétaire notifié |
| **Autre** | Message libre au propriétaire |

### Comportement par statut de connexion

| Statut | Comportement |
|---|---|
| **En ligne (non logué)** | Signal envoyé directement au serveur (anonyme + device_fingerprint). Le bien est masqué localement. |
| **Hors-ligne (PWA)** | Signal stocké en localStorage, synchronisé au retour en ligne via Background Sync API (27.12, wave-09). |
| **Connecté** | Le bien est masqué dans ses résultats. Le signalement est enregistré côté serveur. |
| **Annonceur** | Peut signaler ses propres annonces (changement de statut). |

### Escalade automatique

| Seuil | Action |
|---|---|
| **1 signalement** | Badge "signalement reçu" visible (anonyme). Annonce toujours visible. |
| **2 signalements** (même type) | Notification au propriétaire : "Votre annonce a été signalée X fois. Merci de vérifier." |
| **3+ signalements** (types différents ou personnes différentes) | Annonce **archivée** automatiquement. Non visible dans les résultats. |
| **5+ signalements** | Annonce **supprimée**. L'auteur reçoit un avertissement. |

### Traitement des annonces non automatiques

Pour les annonces déposées manuellement (pas d'import auto) :
- **1er signalement** : Notification email au propriétaire avec lien de mise à jour
- **2ème signalement** : Relance avec mise en garde
- **3ème signalement** : Annonce archivée, propriétaire notifié
- **Sans réponse sous 7 jours** : Annonce supprimée, pénalité sur le score de fiabilité du propriétaire

---

## Score de fiabilité du propriétaire

Un **score de fiabilité** (0-100) est calculé pour chaque annonceur :

| Facteur | Impact |
|---|---|
| Annonces actives sans signalement | +2 points/mois |
| Annonces mises à jour régulièrement | +1 point/mois |
| Signalement reçus | -10 points par signalement |
| Annonces archivées/supprimées pour signalement | -25 points |
| Réponse aux signalements (mise à jour) | +5 points |
| Temps moyen de réponse aux messages | Impact positif |

Le score de fiabilité est visible sur le profil du propriétaire (badge : "Propriétaire fiable" / "Nouveau" / "À vérifier") — détaillé dans l'espace annonceur (wave-11).

Un score < 30 : les annonces de ce propriétaire sont affichées en dernier dans les résultats.
Un score < 10 : les nouvelles annonces de ce propriétaire nécessitent une validation manuelle avant publication.
