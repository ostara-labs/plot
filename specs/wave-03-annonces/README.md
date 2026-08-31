# Wave 03 — Annonces

> Dépôt et gestion des annonces : vecteurs d'ajout, processus de création, récupération de bien (claim) et fiche détaillée. Le signalement par les utilisateurs et le score de fiabilité sont traités dans la [Wave 05 — Confiance](../wave-05-confiance/README.md).

> Retour au [spec principal](../README.md)

---

## 8. Déposer une annonce

### Vecteurs d'ajout

| Vecteur | Qui | Processus |
|---|---|---|
| **Manuel — particulier** | Propriétaire qui veut vendre/louer | Formulaire simple (adresse, type, prix, photos) |
| **Manuel — agence** | Agent immobilier | Formulaire + vérification SIRET |
| **Manuel — notaire** | Notaire en charge d'une vente | Formulaire + vérification immatriculation |
| **Automatique** | Import depuis sources externes | Scraper/API (à specer séparément) |
| **Récupération de bien** | Entreprise qui veut reprendre une annonce existante | Prouver ownership (voir ci-dessous) |

### Processus de création d'annonce

```
[1] Type de bien ─── [2] Localisation ─── [3] Caractéristiques ─── [4] Photos ─── [5] Prix & conditions
     ●                     ○                      ○                      ○                ○
```

#### Étape 1 : Type de bien

| Choix | Description |
|---|---|
| Terrain | Parcelle à vendre |
| Maison | Maison individuelle |
| Appartement | Appartement |

#### Étape 2 : Localisation

- Adresse (auto-géocodage)
- Ou saisie parcelle cadastre (section + numéro)
- Géométrie récupérée depuis la table `terrains` (réplication cadastre locale — 27.9)

#### Étape 3 : Caractéristiques (selon type)

**Terrain :**
| Champ | Obligatoire |
|---|---|
| Surface (m²) | ✅ |
| Constructible | ✅ |
| Pente estimée | Optionnel |
| Exposition | Optionnel |
| Accès eau | Optionnel |
| Accès électricité | Optionnel |
| Description libre | Optionnel |

**Maison :**
| Champ | Obligatoire |
|---|---|
| Surface habitable (m²) | ✅ |
| Nombre de pièces | ✅ |
| Nombre de chambres | ✅ |
| DPE | Recommandé |
| Terrain (m²) | Optionnel |
| Garage / parking | Optionnel |
| Description libre | Optionnel |

**Appartement :**
| Champ | Obligatoire |
|---|---|
| Surface habitable (m²) | ✅ |
| Nombre de pièces | ✅ |
| Nombre de chambres | ✅ |
| Étage | ✅ |
| DPE | Recommandé |
| Ascenseur | Optionnel |
| Balcon / terrasse | Optionnel |
| Description libre | Optionnel |

#### Étape 4 : Photos

- Upload multiple (drag & drop)
- Photo principale = photo de couverture
- Min 1 photo, max 30
- Formats : JPG, PNG, WebP
- Max 10 Mo par photo
- Stockage : gestionnaire objet S3-compatible — la DB ne stocke que les URLs (27.2)

#### Étape 5 : Prix & conditions

| Champ | Obligatoire |
|---|---|
| Prix de vente (€) | ✅ |
| Frais d'agence inclus ? | Toggle |
| Disponibilité | Date ou "Immédiat" |
| Charges mensuelles (si appt) | Optionnel |
| Taxe foncière estimée | Auto-calculée si possible |

### Récupération de bien (claim)

Un professionnel (agence, notaire, particulier) peut **récupérer une annonce existante** si le bien lui appartient ou s'il en est mandataire.

**Processus :**
1. L'utilisateur trouve le bien sur la carte
2. Clique "Ce bien est le mien" ou "Je suis mandataire"
3. Système vérifie :
   - Si le bien a déjà un propriétaire → refus (annonce déjà gérée)
   - Sinon → demander justificatif :
     - **Propriétaire** : acte de propriété ou taxe foncière récente
     - **Mandataire** : mandat de vente signé
     - **Agence** : mandat + SIRET
     - **Notaire** : mandat de vente + immatriculation
4. Vérification manuelle (ou auto si possible)
5. Transfert de propriété de l'annonce

### Gestion des annonces

| Action | Qui | Description |
|---|---|---|
| **Modifier** | Propriétaire de l'annonce | Modifier caractéristiques, prix, photos |
| **Désactiver** | Propriétaire de l'annonce | Masquer temporairement (restorable) |
| **Supprimer** | Propriétaire de l'annonce | Suppression logique, récupérable 30 jours (rétention RGPD — wave-01 §22) |
| **Marquer vendu/loué** | Propriétaire de l'annonce | Changer le statut |
| **Signaler** | Tout utilisateur (y compris déconnecté) | "Ce bien n'est plus disponible" |

---

## 9. Fiche détaillée

### Logement principal

| Section | Contenu |
|---|---|
| **En-tête** | Adresse, score global, prix estimé |
| **Carte** | Localisation exacte, parcelle/bien surligné |
| **Caractéristiques** | Surface, pièces, DPE, etc. (selon catégorie) |
| **Score détaillé** | Barres par critère avec poids |
| **Contexte** | PLU, risques, POI, transactions comparables |
| **Photos** | Photo aérienne (tuiles IGN servies via cache/CDN — 27.9) |
| **Annonce** | Si bien déposé sur Plot : fiche annonce avec contact propriétaire |
| **Signaler** | Bouton "Ce bien n'est plus disponible" |

### Contact vendeur

#### Fonctionnalité

Un utilisateur connecté peut contacter le vendeur/propriétaire d'une annonce.

#### Processus

```
[1] Clic "Contacter" ─── [2] Formulaire ─── [3] Envoi ─── [4] Confirmation
        ●                      ○                ○                ○
```

#### Formulaire de contact

| Champ | Obligatoire | Description |
|---|---|---|
| Nom | ✅ | Pré-rempli si profil complet |
| Email | ✅ | Pré-rempli (masqué au vendeur) |
| Téléphone | Optionnel | Pour contact rapide |
| Message | ✅ | Template pré-rempli : "Bonjour, je suis intéressé par votre bien à [adresse]..." |

#### Protection de la vie privée

| Règle | Description |
|---|---|
| Email masqué | L'email du contacteur est masqué (relais Plot) |
| Pas de spam | Rate limiting : 5 messages/heure |
| Historique | Le vendeur voit l'historique des contacts dans son dashboard (wave-11 — Espace annonceur) |
| Désinscription | Le vendeur peut bloquer un contacteur |

#### Notification vendeur

| Événement | Notification |
|---|---|
| Nouveau message | Email + in-app |
| Message lu | In-app |
| Contacteur a signalé | Email (si le bien est signalé par le contacteur) |

### Investissement

| Section | Contenu |
|---|---|
| **En-tête** | Adresse, rentabilité, prix |
| **Analyse financière** | Prix d'achat, loyer estimé, taxe foncière, charges |
| **Rentabilité** | Brute, nette, cashflow |
| **Marché** | Transactions comparables, évolution prix |
| **Risques** | DPE, risques naturels |
| **Carte** | Localisation + calques |
| **Annonce** | Si bien déposé sur Plot : fiche annonce avec contact propriétaire |
