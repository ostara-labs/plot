"""SQLAlchemy models — import all so ``Base.metadata`` is complete for Alembic.

Every model is re-exported here; importing this module registers all tables
on ``Base.metadata``.
"""

from plot_backend.app.db.models.engagement import (
    Contact,
    Favorite,
    Feedback,
    Notification,
    Share,
)
from plot_backend.app.db.models.geodata import Property, Score, Terrain
from plot_backend.app.db.models.identity import User
from plot_backend.app.db.models.listings import Claim, Listing, Report
from plot_backend.app.db.models.projects import PriorityZone, Project, WeightingProfile

__all__ = [
    "Claim",
    "Contact",
    "Favorite",
    "Feedback",
    "Listing",
    "Notification",
    "PriorityZone",
    "Project",
    "Property",
    "Report",
    "Score",
    "Share",
    "Terrain",
    "User",
    "WeightingProfile",
]
