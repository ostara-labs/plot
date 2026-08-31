# Wave 10 — Langues régionales

> Ajout du support des langues régionales françaises.

> Retour au [spec principal](../README.md)

---

## Contexte

La France compte plusieurs langues régionales qui font partie de son patrimoine culturel. Cette wave ajoute le support de ces langues pour l'interface utilisateur.

## Langues cibles

| Langue | Code | Région |
|---|---|---|
| Breton | `br` | Bretagne |
| Occitan | `oc` | Occitanie |
| Basque | `eu` | Pays basque |
| Corse | `co` | Corse |
| Alsacien | `gsw` | Alsace |
| Créole réunionnais | `rcf` | Réunion |
| Créole guadeloupéen | `gcf` | Guadeloupe |
| Créole martiniquais | `gcf-MQ` | Martinique |
| Créole guyanais | `gcr` | Guyane |

> `gcf-MQ` : variante régionale du créole à base française.

## Stratégie

### Même approche que FR/EN

- Paraglide gère toutes les langues
- Fichiers de traduction séparés par langue : `br.json`, `oc.json`, etc.
- Routing : `/br/...`, `/oc/...`, `/eu/...`
- Détection automatique basée sur la localisation de l'utilisateur (optionnel)

### Priorisation

| Priorité | Langues |
|---|---|
| P0 | Breton, Occitan, Basque |
| P1 | Corse, Alsacien |
| P2 | Créoles |

### Contenu traduit

| Élément | Traduit ? |
|---|---|
| Interface (boutons, labels) | ✅ |
| Messages d'erreur | ✅ |
| Textes de contenu | ❌ (gardé en langue d'origine) |
| Noms de communes | ❌ (gardé tel quel) |

### Démarrage progressif

1. **Phase 1** : FR + EN + Breton + Occitan + Basque
2. **Phase 2** : Ajouter Corse + Alsacien
3. **Phase 3** : Ajouter Créoles

## Notes

- Les langues régionales ne sont pas obligatoires pour le MVP
- Le contenu généré par les utilisateurs reste dans la langue d'origine
- L'API peut retourner des métadonnées dans la langue demandée (paramètre `Accept-Language`)
