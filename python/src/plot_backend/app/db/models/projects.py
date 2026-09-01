"""Project domain: ``projects``, ``priority_zones``, ``weighting_profiles``."""

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import DateTime, Float, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    PriorityLevel,
    ProjectCategory,
    ProjectType,
    enum_column,
)


class Project(Base):
    """A saved search with its criteria (spec wave-01 §13)."""

    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(Text)
    project_type: Mapped[ProjectType] = mapped_column(enum_column(ProjectType, "project_type"))
    category: Mapped[ProjectCategory] = mapped_column(
        enum_column(ProjectCategory, "project_category")
    )
    criteria: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB))
    zone: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    zone_lambert_93: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=2154, spatial_index=True)
    )
    zone_center: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )
    zone_center_lambert_93: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="POINT", srid=2154, spatial_index=True)
    )
    zone_radius_in_kilometers: Mapped[float | None] = mapped_column(Float, index=True)
    max_budget_in_euros: Mapped[float | None] = mapped_column(Float, index=True)
    latest_results: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB))
    new_offers_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_viewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class PriorityZone(Base):
    """A priority zone drawn on the investment map (wave-04)."""

    __tablename__ = "priority_zones"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"), index=True)
    level: Mapped[PriorityLevel] = mapped_column(enum_column(PriorityLevel, "priority_level"))
    geometry: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True)
    )
    geometry_lambert_93: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=2154, spatial_index=True)
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WeightingProfile(Base):
    """A saved weighting profile, reusable across projects (wave-04)."""

    __tablename__ = "weighting_profiles"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(Text)
    category: Mapped[ProjectCategory] = mapped_column(
        enum_column(ProjectCategory, "profile_category")
    )
    weights: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
