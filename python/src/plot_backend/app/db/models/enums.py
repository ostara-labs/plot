"""Shared enum types for the Plot data model.

Each enum maps to a dedicated PostgreSQL native enum type (explicit ``name``
avoids collisions). ``values_callable`` stores the member *value* (the exact
string from the spec) rather than the member name.
"""

import enum

from sqlalchemy import Enum as SAEnum


def enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    """Return the string values of an enum class, for ``values_callable``."""
    return [member.value for member in enum_cls]


class UserType(enum.Enum):
    particulier = "particulier"
    agence = "agence"
    notaire = "notaire"


class UserRole(enum.Enum):
    user = "user"
    moderateur = "moderateur"
    admin = "admin"


class ProjetType(enum.Enum):
    logement = "logement"
    investissement = "investissement"


class Categorie(enum.Enum):
    terrain_terre = "terrain-terre"
    terrain_classique = "terrain-classique"
    maison = "maison"
    appartement = "appartement"


class ZonePrioriteNiveau(enum.Enum):
    haute = "haute"
    moyenne = "moyenne"
    basse = "basse"


class TerrainZone(enum.Enum):
    urbain = "urbain"
    periurbain = "periurbain"
    rural = "rural"


class BienType(enum.Enum):
    maison = "maison"
    appartement = "appartement"


class TargetType(enum.Enum):
    terrain = "terrain"
    bien = "bien"


class AnnonceType(enum.Enum):
    terrain = "terrain"
    maison = "maison"
    appartement = "appartement"


class AnnonceStatut(enum.Enum):
    active = "active"
    sous_offre = "sous_offre"
    vendu = "vendu"
    loue = "loué"
    archivee = "archivée"
    desactivee = "désactivée"
    supprimee = "supprimée"
    signalee = "signalée"


class AnnonceSource(enum.Enum):
    manuel = "manuel"
    import_ = "import"
    claim = "claim"


class AnnonceClaimStatus(enum.Enum):
    none = "none"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class SignalementType(enum.Enum):
    vendu = "vendu"
    sous_offre = "sous_offre"
    faux = "faux"
    erreur_prix = "erreur_prix"
    autre = "autre"


class SignalementStatut(enum.Enum):
    en_attente = "en_attente"
    traite = "traite"
    rejete = "rejeté"


class ClaimType(enum.Enum):
    proprietaire = "proprietaire"
    mandataire = "mandataire"
    agence = "agence"
    notaire = "notaire"


class ClaimStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class FeedbackType(enum.Enum):
    bug = "bug"
    idee = "idee"
    question = "question"
    doleance = "doléance"


class FeedbackStatus(enum.Enum):
    nouveau = "nouveau"
    en_cours = "en_cours"
    traite = "traite"
    archive = "archive"


class PartageType(enum.Enum):
    projet = "projet"
    compare = "compare"
    carte = "carte"


class NotificationType(enum.Enum):
    nouvelle_offre = "nouvelle_offre"
    mise_a_jour = "mise_a_jour"
    annonce_statut = "annonce_statut"
    signalement = "signalement"
    contact = "contact"
    compte = "compte"
    recap_hebdo = "recap_hebdo"


def enum_column(enum_cls: type[enum.Enum], name: str) -> SAEnum:
    """Build a native PostgreSQL enum column type with explicit name."""
    return SAEnum(enum_cls, name=name, values_callable=enum_values)
