"""Geodata domain: ``terrains``, ``properties``, ``scores`` (open data + scoring)."""

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import Boolean, DateTime, Float, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    PropertyType,
    TargetType,
    TerrainZone,
    enum_column,
)


class Terrain(Base):
    """A cadastral parcel enriched with open data (spec wave-01 §13)."""

    __tablename__ = "terrains"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    parcel_id: Mapped[str] = mapped_column(Text, index=True)
    commune: Mapped[str] = mapped_column(Text, index=True)
    surface_in_square_meters: Mapped[float | None] = mapped_column(Float, index=True)
    geometry: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    geometry_lambert_93: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=2154, spatial_index=True)
    )
    zone: Mapped[TerrainZone | None] = mapped_column(
        enum_column(TerrainZone, "terrain_zone"), index=True
    )
    buildable: Mapped[bool | None] = mapped_column(Boolean, index=True)
    estimated_price_in_euros: Mapped[float | None] = mapped_column(Float, index=True)
    property_tax_in_euros: Mapped[float | None] = mapped_column(Float, index=True)
    slope_in_percent: Mapped[float | None] = mapped_column(Float, index=True)
    exposure: Mapped[str | None] = mapped_column(Text, index=True)
    # DB column name is ``metadata`` (spec); ``metadata_json`` avoids the
    # reserved ``metadata`` attribute on the Declarative API. MutableDict
    # tracks in-place dict mutations (ETL enrichment) so they persist.
    metadata_json: Mapped[dict | None] = mapped_column("metadata", MutableDict.as_mutable(JSONB))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Property(Base):
    """A house or apartment from open data (spec wave-01 §13)."""

    __tablename__ = "properties"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    property_type: Mapped[PropertyType] = mapped_column(enum_column(PropertyType, "property_type"))
    address: Mapped[str | None] = mapped_column(Text)
    commune: Mapped[str] = mapped_column(Text, index=True)
    surface_in_square_meters: Mapped[float | None] = mapped_column(Float, index=True)
    price_in_euros: Mapped[float | None] = mapped_column(Float, index=True)
    geometry: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
    geometry_lambert_93: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=2154, spatial_index=True)
    )
    energy_performance_class: Mapped[str | None] = mapped_column(Text, index=True)
    greenhouse_gas_class: Mapped[str | None] = mapped_column(Text, index=True)
    potential_rent_in_euros: Mapped[float | None] = mapped_column(Float, index=True)
    property_tax_in_euros: Mapped[float | None] = mapped_column(Float, index=True)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", MutableDict.as_mutable(JSONB))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Score(Base):
    """A computed score for a terrain or property (spec wave-01 §13)."""

    __tablename__ = "scores"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    target_type: Mapped[TargetType] = mapped_column(enum_column(TargetType, "score_target_type"))
    target_id: Mapped[UUID] = mapped_column(index=True)
    category: Mapped[str] = mapped_column(Text, index=True)
    score: Mapped[float] = mapped_column(Float, index=True)
    breakdown: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB))
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
