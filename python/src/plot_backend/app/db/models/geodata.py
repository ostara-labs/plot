"""Geodata domain: ``terrains``, ``biens``, ``scores`` (open data + scoring)."""

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import Boolean, DateTime, Float, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    BienType,
    TargetType,
    TerrainZone,
    enum_column,
)


class Terrain(Base):
    """A cadastral parcel enriched with open data (spec wave-01 §13)."""

    __tablename__ = "terrains"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    parcelle_id: Mapped[str] = mapped_column(Text, index=True)
    commune: Mapped[str] = mapped_column(Text, index=True)
    surface_m2: Mapped[float | None] = mapped_column(Float, index=True)
    geometry: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    geometry_2154: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=2154, spatial_index=True)
    )
    zone: Mapped[TerrainZone | None] = mapped_column(
        enum_column(TerrainZone, "terrain_zone"), index=True
    )
    buildable: Mapped[bool | None] = mapped_column(Boolean, index=True)
    estimated_price_eur: Mapped[float | None] = mapped_column(Float, index=True)
    taxe_fonciere_eur: Mapped[float | None] = mapped_column(Float, index=True)
    slope_pct: Mapped[float | None] = mapped_column(Float, index=True)
    exposure: Mapped[str | None] = mapped_column(Text, index=True)
    # DB column name is ``metadata`` (spec); ``metadata_json`` avoids the
    # reserved ``metadata`` attribute on the Declarative API.
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Bien(Base):
    """A house or apartment from open data (spec wave-01 §13)."""

    __tablename__ = "biens"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    type: Mapped[BienType] = mapped_column(enum_column(BienType, "bien_type"))
    address: Mapped[str | None] = mapped_column(Text)
    commune: Mapped[str] = mapped_column(Text, index=True)
    surface_m2: Mapped[float | None] = mapped_column(Float, index=True)
    price_eur: Mapped[float | None] = mapped_column(Float, index=True)
    geometry: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
    geometry_2154: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=2154, spatial_index=True)
    )
    dpe: Mapped[str | None] = mapped_column(Text, index=True)
    ges: Mapped[str | None] = mapped_column(Text, index=True)
    loyer_potentiel_eur: Mapped[float | None] = mapped_column(Float, index=True)
    taxe_fonciere_eur: Mapped[float | None] = mapped_column(Float, index=True)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Score(Base):
    """A computed score for a terrain or bien (spec wave-01 §13)."""

    __tablename__ = "scores"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    target_type: Mapped[TargetType] = mapped_column(enum_column(TargetType, "score_target_type"))
    target_id: Mapped[UUID] = mapped_column(index=True)
    category: Mapped[str] = mapped_column(Text, index=True)
    score: Mapped[float] = mapped_column(Float, index=True)
    breakdown: Mapped[dict | None] = mapped_column(JSONB)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
