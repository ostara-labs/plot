"""Project domain: ``projets``, ``zones_priorite``, ``profils_ponderation``."""

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import DateTime, Float, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    Categorie,
    ProjetType,
    ZonePrioriteNiveau,
    enum_column,
)


class Projet(Base):
    """A saved search with its criteria (spec wave-01 §13)."""

    __tablename__ = "projets"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    nom: Mapped[str] = mapped_column(Text)
    type: Mapped[ProjetType] = mapped_column(enum_column(ProjetType, "projet_type"))
    categorie: Mapped[Categorie] = mapped_column(enum_column(Categorie, "projet_categorie"))
    criteres: Mapped[dict | None] = mapped_column(JSONB)
    zone: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    zone_2154: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=2154, spatial_index=True)
    )
    zone_centre: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
    zone_centre_2154: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=2154, spatial_index=True)
    )
    zone_rayon_km: Mapped[float | None] = mapped_column(Float, index=True)
    budget_max: Mapped[float | None] = mapped_column(Float, index=True)
    derniers_resultats: Mapped[dict | None] = mapped_column(JSONB)
    nouvelles_offres: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    date_creation: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    date_derniere_consultation: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    date_mise_a_jour: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ZonePriorite(Base):
    """A priority zone drawn on the investment map (wave-04)."""

    __tablename__ = "zones_priorite"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    projet_id: Mapped[UUID] = mapped_column(ForeignKey("projets.id"), index=True)
    niveau: Mapped[ZonePrioriteNiveau] = mapped_column(
        enum_column(ZonePrioriteNiveau, "zone_priorite_niveau")
    )
    geometry: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    geometry_2154: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=2154, spatial_index=True)
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProfilPonderation(Base):
    """A saved weighting profile, reusable across projects (wave-04)."""

    __tablename__ = "profils_ponderation"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    nom: Mapped[str] = mapped_column(Text)
    categorie: Mapped[Categorie] = mapped_column(enum_column(Categorie, "profil_categorie"))
    poids: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
