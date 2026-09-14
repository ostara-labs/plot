"""Pydantic schemas for the fastapi-users flows.

Kept minimal (email + password + lifecycle flags): the profile fields
(last_name, first_name, type, siret) belong to the deferred registration
step 3 (spec wave-01 §20) and are added when that flow ships.
"""

from uuid import UUID

from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    """Public representation of a user."""


class UserCreate(schemas.BaseUserCreate):
    """Payload for ``POST /auth/register``."""


class UserUpdate(schemas.BaseUserUpdate):
    """Payload for ``PATCH /users/me``."""
