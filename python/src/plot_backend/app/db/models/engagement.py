"""Engagement domain: feedback, contacts, favorites, shares, notifications."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import (
    FeedbackStatus,
    FeedbackType,
    NotificationType,
    ShareType,
    TargetType,
    enum_column,
)


class Feedback(Base):
    """In-app user feedback (spec wave-01 §13, decision 27.26)."""

    __tablename__ = "feedback"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    tracking_token: Mapped[str | None] = mapped_column(Text, index=True)
    feedback_type: Mapped[FeedbackType] = mapped_column(enum_column(FeedbackType, "feedback_type"))
    message: Mapped[str] = mapped_column(Text)
    page: Mapped[str | None] = mapped_column(Text)
    context: Mapped[dict | None] = mapped_column(JSONB)
    status: Mapped[FeedbackStatus] = mapped_column(
        enum_column(FeedbackStatus, "feedback_status"),
        default=FeedbackStatus.NEW,
        server_default="new",
    )
    response: Mapped[str | None] = mapped_column(Text)
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Contact(Base):
    """A buyer-to-seller message (wave-03, rate limited via Redis)."""

    __tablename__ = "contacts"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    listing_id: Mapped[UUID] = mapped_column(ForeignKey("listings.id"), index=True)
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    message: Mapped[str] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Favorite(Base):
    """A favorited terrain or property (wave-02, polymorphic target)."""

    __tablename__ = "favorites"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    target_type: Mapped[TargetType] = mapped_column(enum_column(TargetType, "favorite_target_type"))
    target_id: Mapped[UUID] = mapped_column(index=True)
    project_id: Mapped[UUID | None] = mapped_column(ForeignKey("projects.id"), index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Share(Base):
    """A share link identified by a public token (wave-02)."""

    __tablename__ = "shares"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    token: Mapped[str] = mapped_column(Text, unique=True, index=True)
    share_type: Mapped[ShareType] = mapped_column(enum_column(ShareType, "share_type"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    target_id: Mapped[UUID] = mapped_column()
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    """An in-app notification (wave-07)."""

    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    notification_type: Mapped[NotificationType] = mapped_column(
        enum_column(NotificationType, "notification_type")
    )
    title: Mapped[str] = mapped_column(Text)
    message: Mapped[str | None] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(Text)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
