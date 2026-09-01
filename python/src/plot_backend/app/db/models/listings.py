"""Listings domain: ``listings``, ``reports``, ``claims``."""

from datetime import datetime
from uuid import UUID

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    ClaimStatus,
    ClaimType,
    ListingClaimStatus,
    ListingSource,
    ListingStatus,
    ListingType,
    ReportStatus,
    ReportType,
    enum_column,
)


class Listing(Base):
    """A listing created by a user (spec wave-01 §13)."""

    __tablename__ = "listings"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[ListingType] = mapped_column(enum_column(ListingType, "listing_type"))
    status: Mapped[ListingStatus] = mapped_column(
        enum_column(ListingStatus, "listing_status"),
        default=ListingStatus.ACTIVE,
        server_default="active",
        index=True,
    )
    address: Mapped[str | None] = mapped_column(Text)
    commune: Mapped[str | None] = mapped_column(Text, index=True)
    geometry: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="GEOMETRY", srid=4326, spatial_index=True)
    )
    geometry_lambert_93: Mapped[WKBElement | None] = mapped_column(
        Geometry(geometry_type="GEOMETRY", srid=2154, spatial_index=True)
    )
    price_in_euros: Mapped[float | None] = mapped_column(index=True)
    surface_in_square_meters: Mapped[float | None] = mapped_column(index=True)
    energy_performance_class: Mapped[str | None] = mapped_column(Text, index=True)
    bedrooms: Mapped[int | None] = mapped_column(Integer, index=True)
    photos: Mapped[dict | None] = mapped_column(JSONB)
    features: Mapped[dict | None] = mapped_column(JSONB)
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[ListingSource] = mapped_column(
        enum_column(ListingSource, "listing_source"),
        default=ListingSource.MANUAL,
        server_default="manual",
    )
    claim_status: Mapped[ListingClaimStatus] = mapped_column(
        enum_column(ListingClaimStatus, "listing_claim_status"),
        default=ListingClaimStatus.NONE,
        server_default="none",
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    report_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0", index=True)


class Report(Base):
    """A user report that a listing is unavailable (spec wave-01 §13)."""

    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    listing_id: Mapped[UUID] = mapped_column(ForeignKey("listings.id"), index=True)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    device_fingerprint: Mapped[str | None] = mapped_column(Text, index=True)
    type: Mapped[ReportType] = mapped_column(enum_column(ReportType, "report_type"))
    message: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ReportStatus] = mapped_column(
        enum_column(ReportStatus, "report_status"),
        default=ReportStatus.PENDING,
        server_default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Claim(Base):
    """A request to take ownership of an existing listing (spec wave-01 §13)."""

    __tablename__ = "claims"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    listing_id: Mapped[UUID] = mapped_column(ForeignKey("listings.id"), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[ClaimType] = mapped_column(enum_column(ClaimType, "claim_type"))
    proof_document_url: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ClaimStatus] = mapped_column(
        enum_column(ClaimStatus, "claim_status"),
        default=ClaimStatus.PENDING,
        server_default="pending",
    )
    admin_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
