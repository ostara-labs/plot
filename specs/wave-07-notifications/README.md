# Wave 07 — Notifications

> Système de notifications : email, push, in-app et templates transactionnels.

> Retour au [spec principal](../README.md)

---

## 27. Notifications

### Types de notifications

| Type | Canal | Description |
|---|---|---|
| **Nouvelle offre** | Email + Push + In-app | Nouveau bien correspondant au projet |
| **Mise à jour offre** | In-app | Prix changé, photos ajoutées |
| **Annonce vendue/louée** | Email + In-app | Le bien d'un favori a été vendu/loué |
| **Signalement** | Email + In-app | Votre annonce a été signalée |
| **Réponse contact** | Email + In-app | Un vendeur a répondu à votre message |
| **Compte** | Email | Vérification, reset MDP, bienvenue |
| **Récap hebdo** | Email | Résumé des nouvelles offres de vos projets |

### Fréquence (configurable par l'utilisateur)

| Paramètre | Options | Défaut |
|---|---|---|
| Nouvelles offres | Instantané / Quotidien / Hebdomadaire | Quotidien |
| Récap hebdo | Oui / Non | Oui |
| Alertes compte | Toujours (non désactivable) | — |

### Canaux

| Canal | Description | Configuration |
|---|---|---|
| **Email** | Notifications par email | Adresse email vérifiée |
| **Push** | Notifications navigateur (Web Push API) | Consentement utilisateur |
| **In-app** | Badge + centre de notifications | Toujours actif |

### Centre de notifications

```
┌─────────────────────────────────────┐
│  🔔 Notifications (3 non lues)      │
├─────────────────────────────────────┤
│  🔴 Terrain 800m² à Carcassonne    │
│     Nouveau bien pour "Terrain Aude"│
│     il y a 2h                       │
├─────────────────────────────────────┤
│  🟡 Votre annonce a été signalée   │
│     15 Rue de la Paix, Paris       │
│     il y a 1 jour                   │
├─────────────────────────────────────┤
│  🟢 Message de Jean D.             │
│     Concernant : Maison Colmar      │
│     il y a 3 jours                  │
└─────────────────────────────────────┘
```

### Push notifications

| Technologie | Description |
|---|---|
| Web Push API | Notifications navigateur (Chrome, Firefox, Edge) |
| Service Worker | Réception même si l'onglet est fermé |
| FCM / Web Push Protocol | Envoi côté serveur |

### Table `notifications`

| Colonne | Type | Description |
|---|---|---|
| id | UUID | PK |
| user_id | UUID | FK users |
| type | ENUM | nouvelle_offre, mise_a_jour, signalement, contact, compte |
| titre | TEXT | Titre court |
| message | TEXT | Description |
| lien | TEXT | URL de destination |
| lu | BOOLEAN | Notification lue |
| created_at | TIMESTAMPTZ | |

---

## 28. Emails transactionnels

### Templates

| Template | Trigger | Contenu |
|---|---|---|
| **Bienvenue** | Inscription | Lien vérification, introduction |
| **Vérification email** | Inscription / Changement email | Lien vérification (24h) |
| **Reset MDP** | Demande reset | Lien reset (1h) |
| **Nouvelle offre** | Projet match | Liste des nouveaux biens |
| **Récap hebdo** | Chaque lundi | Résumé de la semaine |
| **Signalement reçu** | Annonce signalée | Détails du signalement |
| **Contact vendeur** | Nouveau message | Message + coordonnées |
| **Réponse vendeur** | Réponse reçue | Message du vendeur |

### Outil

- **Postmark** — transactionnel + digest
- Templates HTML responsive (Postmark Message Streams)
- Prévisualisation dans le dashboard
- Data aux US, DPA/SCCs pour conformité RGPD

### Désinscription

- Lien "Se désinscrire" dans chaque email
- Préférences de notification configurables dans le profil
- Désinscription légale (CAN-SPAM / RGPD)

---

## 29. SMS transactionnels

### Cas d'usage

| Cas | Type | Description |
|---|---|---|
| **Code OTP** | Transactionnel | Vérification téléphone |
| **Alertes compte** | Transactionnel | Connexion suspecte, changement MDP |
| **Alerte nouvelle offre** | Transactionnel | (optionnel) SMS si utilisateur le souhaite |

### Outil

- **SMSemode (Sarbacane)** — opérateur ARCEP, routing direct
- Data hébergée en France (Tier-4, ISO 27001/27701)
- Prix : from €0.0312/SMS (volume), ~€0.04-0.06 en faible volume
- Subscriptions from €9 HT/mois

### Intégration FastAPI

```python
import httpx

SMSMODE_API_KEY = "your-api-key"

async def send_sms(phone: str, message: str) -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.smsmode.com/http/1.6/sendSMS.do",
            params={
                "apiKey": SMSMODE_API_KEY,
                "sms": message,
                "numero": phone,
                "emetteur": "Plot",
                "sent": "true",  # transactionnel
            },
            timeout=10.0,
        )
        resp.raise_for_status()
```
