"""Shared enum types for the Plot data model.

Every identifier is English (naming convention, decision 27.27): class names,
member names and stored values alike. Each enum maps to a dedicated
PostgreSQL native enum type (explicit ``name`` avoids collisions).
``values_callable`` stores the member *value* rather than the member name.
"""

import enum

from sqlalchemy import Enum as SAEnum


def enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    """Return the string values of an enum class, for ``values_callable``."""
    return [member.value for member in enum_cls]


class UserType(enum.Enum):
    INDIVIDUAL = "individual"
    AGENCY = "agency"
    NOTARY = "notary"


class UserRole(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class ProjectType(enum.Enum):
    HOUSING = "housing"
    INVESTMENT = "investment"


class ProjectCategory(enum.Enum):
    BURIED_TERRAIN = "buried-terrain"
    CLASSIC_TERRAIN = "classic-terrain"
    HOUSE = "house"
    APARTMENT = "apartment"


class PriorityLevel(enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TerrainZone(enum.Enum):
    URBAN = "urban"
    PERIURBAN = "periurban"
    RURAL = "rural"


class PropertyType(enum.Enum):
    HOUSE = "house"
    APARTMENT = "apartment"


class TargetType(enum.Enum):
    TERRAIN = "terrain"
    PROPERTY = "property"


class ListingType(enum.Enum):
    TERRAIN = "terrain"
    HOUSE = "house"
    APARTMENT = "apartment"


class ListingStatus(enum.Enum):
    ACTIVE = "active"
    UNDER_OFFER = "under_offer"
    SOLD = "sold"
    RENTED = "rented"
    ARCHIVED = "archived"
    DISABLED = "disabled"
    DELETED = "deleted"
    REPORTED = "reported"


class ListingSource(enum.Enum):
    MANUAL = "manual"
    IMPORT = "import"
    CLAIM = "claim"


class ListingClaimStatus(enum.Enum):
    NONE = "none"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReportType(enum.Enum):
    SOLD = "sold"
    UNDER_OFFER = "under_offer"
    FRAUD = "fraud"
    PRICE_ERROR = "price_error"
    OTHER = "other"


class ReportStatus(enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    REJECTED = "rejected"


class ClaimType(enum.Enum):
    OWNER = "owner"
    AGENT = "agent"
    AGENCY = "agency"
    NOTARY = "notary"


class ClaimStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class FeedbackType(enum.Enum):
    BUG = "bug"
    IDEA = "idea"
    QUESTION = "question"
    COMPLAINT = "complaint"


class FeedbackStatus(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    PROCESSED = "processed"
    ARCHIVED = "archived"


class ShareType(enum.Enum):
    PROJECT = "project"
    COMPARISON = "comparison"
    MAP = "map"


class NotificationType(enum.Enum):
    NEW_OFFER = "new_offer"
    UPDATE = "update"
    LISTING_STATUS = "listing_status"
    REPORT = "report"
    CONTACT = "contact"
    ACCOUNT = "account"
    WEEKLY_DIGEST = "weekly_digest"


def enum_column(enum_cls: type[enum.Enum], name: str) -> SAEnum:
    """Build a native PostgreSQL enum column type with explicit name."""
    return SAEnum(enum_cls, name=name, values_callable=enum_values)
