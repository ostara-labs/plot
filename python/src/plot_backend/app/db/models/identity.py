"""Identity domain: ``users`` table (spec wave-01 §13)."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from plot_backend.app.db.base import Base
from plot_backend.app.db.models.enums import UserRole, UserType, enum_column


class User(Base):
    """A Plot account: particulier, agence or notaire."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    email: Mapped[str] = mapped_column(Text, unique=True, index=True)
    nom: Mapped[str | None] = mapped_column(Text)
    prenom: Mapped[str | None] = mapped_column(Text)
    type: Mapped[UserType | None] = mapped_column(enum_column(UserType, "user_type"))
    siret: Mapped[str | None] = mapped_column(Text)
    role: Mapped[UserRole] = mapped_column(
        enum_column(UserRole, "user_role"),
        default=UserRole.user,
        server_default="user",
    )
    bloque: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    email_verifie: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    score_fiabilite: Mapped[float | None] = mapped_column(Float)
    locale: Mapped[str] = mapped_column(String(10), default="fr", server_default="fr")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
