# Glossary

The ubiquitous language of Plot: one entry per term, with what it is
NOT. Identifiers in code follow the same words (naming convention,
decision 27.27) — if the vocabulary here and in code diverge, that is a
bug: fix it.

- **Terrain** — a cadastral parcel, enriched with open data (taxe
  foncière, pente, exposition, constructibilité). NOT a user-published
  offer, NOT necessarily for sale.
- **Property** — a house or apartment known from open data (price,
  surface, DPE, rent potential). NOT a listing.
- **Listing** — an offer published by a user on a terrain, house or
  apartment (`listing_type`), with a lifecycle (active → under offer →
  sold/rented…). A listing may reference a terrain or property only
  indirectly (address/geometry), never by foreign key.
- **Report** — a user signal that a listing is no longer available
  (sold, fraud, price error…). Aggregated into `listings.report_count`.
- **Claim** — a request by a user to take ownership of an existing
  listing (as owner, agent, agency or notary), with a proof document.
  NOT the listing itself; approval flips the listing's claim status.
- **Project** — a saved search: type (housing / investment), category,
  criteria, and an optional geographic zone (polygon or center+radius).
  NOT a favorite, NOT a share.
- **Priority zone** — a polygon drawn on the investment map, attached to
  a project, with a priority level (high / medium / low).
- **Weighting profile** — a named, reusable set of scoring weights per
  project category, attached to a user.
- **Score** — a computed value for a terrain or a property (polymorphic
  target), per category, with a JSON breakdown of its components.
- **Favorite** — a bookmark on a polymorphic target (terrain, property,
  listing), optionally attached to a project.
- **Share** — a public link identified by a unique token, expirable and
  revocable, pointing at a project, a comparison or a map view.
- **Contact** — a buyer-to-seller message on a listing.
- **Feedback** — in-app user feedback (bug, idea, question, complaint),
  possibly anonymous, tracked by a token.
- **Notification** — an in-app notification for a user (new offer,
  status change, weekly digest…).
- **Commune** — the French administrative commune (proper name, stays
  French), used for indexing and filtering.
- **Account type** — what a user IS: individual, agency or notary
  (agencies and notaries carry a SIRET).
- **Role** — what a user may DO in the app: user, moderator, admin.
  Independent from account type.
- **Reliability score** — a float measuring how trustworthy a user's
  contributions are; populated by later waves, nullable meanwhile.
- **Blocked** — a moderation flag (`is_blocked`) set by a moderator;
  independent from `is_active` (the login lifecycle flag).
