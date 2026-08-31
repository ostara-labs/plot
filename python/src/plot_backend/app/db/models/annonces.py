"""Annonces domain: ``annonces``, ``signalements``, ``claims``."""

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    AnnonceClaimStatus,
    AnnonceSource,
    AnnonceStatut,
    AnnonceType,
    ClaimStatus,
    ClaimType,
    SignalementStatut,
    SignalementType,
    enum_column,
)


class Annonce(Base):
    """A listing created by a user (spec wave-01 §13)."""

    __tablename__ = "annonces"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[AnnonceType] = mapped_column(enum_column(AnnonceType, "annonce_type"))
    statut: Mapped[AnnonceStatut] = mapped_column(
        enum_column(AnnonceStatut, "annonce_statut"),
        default=AnnonceStatut.active,
        server_default="active",
        index=True,
    )
    address: Mapped[str | None] = mapped_column(Text)
    commune: Mapped[str | None] = mapped_column(Text, index=True)
    geometry: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="GEOMETRY", srid=4326, spatial_index=True)
    )
    geometry_2154: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="GEOMETRY", srid=2154, spatial_index=True)
    )
    price_eur: Mapped[float | None] = mapped_column(index=True)
    surface_m2: Mapped[float | None] = mapped_column(index=True)
    dpe: Mapped[str | None] = mapped_column(Text, index=True)
    chambres: Mapped[int | None] = mapped_column(Integer, index=True)
    photos: Mapped[dict | None] = mapped_column(JSONB)
    caracteristiques: Mapped[dict | None] = mapped_column(JSONB)
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[AnnonceSource] = mapped_column(
        enum_column(AnnonceSource, "annonce_source"),
        default=AnnonceSource.manuel,
        server_default="manuel",
    )
    claim_status: Mapped[AnnonceClaimStatus] = mapped_column(
        enum_column(AnnonceClaimStatus, "annonce_claim_status"),
        default=AnnonceClaimStatus.none,
        server_default="none",
    )
    date_depot: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_mise_a_jour: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    date_derniere_verification: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    nombre_signalements: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", index=True
    )


class Signalement(Base):
    """A user report that an annonce is unavailable (spec wave-01 §13)."""

    __tablename__ = "signalements"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    annonce_id: Mapped[UUID] = mapped_column(ForeignKey("annonces.id"), index=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    device_fingerprint: Mapped[str | None] = mapped_column(Text, index=True)
    type: Mapped[SignalementType] = mapped_column(enum_column(SignalementType, "signalement_type"))
    message: Mapped[str | None] = mapped_column(Text)
    statut: Mapped[SignalementStatut] = mapped_column(
        enum_column(SignalementStatut, "signalement_statut"),
        default=SignalementStatut.en_attente,
        server_default="en_attente",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Claim(Base):
    """A request to take ownership of an existing bien (spec wave-01 §13)."""

    __tablename__ = "claims"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    annonce_id: Mapped[UUID] = mapped_column(ForeignKey("annonces.id"), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[ClaimType] = mapped_column(enum_column(ClaimType, "claim_type"))
    justificatif_url: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ClaimStatus] = mapped_column(
        enum_column(ClaimStatus, "claim_status"),
        default=ClaimStatus.pending,
        server_default="pending",
    )
    note_admin: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
