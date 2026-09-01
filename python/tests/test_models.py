"""Model metadata smoke tests: all spec tables and geometry companions."""

from plot_backend.app.db import models  # noqa: F401 — register all tables
from plot_backend.app.db.base import Base

EXPECTED_TABLES = {
    "users",
    "projects",
    "priority_zones",
    "weighting_profiles",
    "terrains",
    "properties",
    "scores",
    "listings",
    "reports",
    "claims",
    "feedback",
    "contacts",
    "favorites",
    "shares",
    "notifications",
}

# (table, 4326 column, Lambert-93 companion) per spec note 27.3.
GEOMETRY_PAIRS = [
    ("projects", "zone", "zone_lambert_93"),
    ("projects", "zone_center", "zone_center_lambert_93"),
    ("priority_zones", "geometry", "geometry_lambert_93"),
    ("terrains", "geometry", "geometry_lambert_93"),
    ("properties", "geometry", "geometry_lambert_93"),
    ("listings", "geometry", "geometry_lambert_93"),
]


def test_all_spec_tables_present():
    assert EXPECTED_TABLES <= set(Base.metadata.tables)


def test_geometry_columns_have_lambert_93_companions():
    tables = Base.metadata.tables
    for table_name, geom_col, companion in GEOMETRY_PAIRS:
        table = tables[table_name]
        assert geom_col in table.columns, f"{table_name}.{geom_col} missing"
        assert companion in table.columns, f"{table_name}.{companion} missing"
        assert table.columns[geom_col].type.srid == 4326
        assert table.columns[companion].type.srid == 2154
