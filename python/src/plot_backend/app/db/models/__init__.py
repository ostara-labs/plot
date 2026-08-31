"""SQLAlchemy models — import all so ``Base.metadata`` is complete for Alembic.

Every model is re-exported here; importing this module registers all tables
on ``Base.metadata``.
"""

from plot_backend.app.db.models.annonces import Annonce, Claim, Signalement
from plot_backend.app.db.models.engagement import (
    Contact,
    Favori,
    Feedback,
    Notification,
    Partage,
)
from plot_backend.app.db.models.geodata import Bien, Score, Terrain
from plot_backend.app.db.models.identity import User
from plot_backend.app.db.models.projets import ProfilPonderation, Projet, ZonePriorite

__all__ = [
    "Annonce",
    "Bien",
    "Claim",
    "Contact",
    "Favori",
    "Feedback",
    "Notification",
    "Partage",
    "ProfilPonderation",
    "Projet",
    "Score",
    "Signalement",
    "Terrain",
    "User",
    "ZonePriorite",
]
