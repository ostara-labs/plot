"""Identity domain: ``users`` table (spec wave-01 §13)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import UserRole, UserType, enum_column


class User(Base):
    """A Plot account: individual, agency or notary.

    ``is_active``/``is_superuser``/``is_verified`` are the fastapi-users
    lifecycle flags. A blocked user keeps ``is_active=True`` until a moderator
    acts: ``is_blocked`` is the moderation flag (wave-08) and does not gate
    fastapi-users login.
    """

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    email: Mapped[str] = mapped_column(Text, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str | None] = mapped_column(Text)
    first_name: Mapped[str | None] = mapped_column(Text)
    type: Mapped[UserType | None] = mapped_column(enum_column(UserType, "user_type"))
    siret: Mapped[str | None] = mapped_column(Text)
    role: Mapped[UserRole] = mapped_column(
        enum_column(UserRole, "user_role"),
        default=UserRole.USER,
        server_default="user",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    is_verified: Mapped[bool] = mapped_column(
        "email_verified", Boolean, default=False, server_default="false", nullable=False
    )
    reliability_score: Mapped[float | None] = mapped_column(Float)
    locale: Mapped[str] = mapped_column(String(10), default="fr", server_default="fr")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
