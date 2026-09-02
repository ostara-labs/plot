"""Alembic environment — wired to Plot settings and models.

The database URL comes from ``plot_backend.app.config.Settings`` (env prefix
``PLOT_``), never from alembic.ini. GeoAlchemy2 helpers make autogenerate
render spatial indexes correctly.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from geoalchemy2 import alembic_helpers
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from plot_backend.app.config import get_settings
from plot_backend.app.db import models  # noqa: F401 — register all tables
from plot_backend.app.db.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", get_settings().database_url.replace("%", "%%"))

target_metadata = Base.metadata


def _object_schema(obj) -> str | None:
    """Return the schema of an autogenerate object (Table/Column/Index/...)."""
    table = getattr(obj, "table", None)
    if table is not None:
        return table.schema
    return getattr(obj, "schema", None)


def include_name(name, type_, parent_names) -> bool:
    """Only compare the default (``public``) schema — skip PostGIS tiger/topology.

    ``None`` is the connection's default schema reported unqualified depending
    on search_path settings; it must be accepted or autogenerate would drop
    every application table.
    """
    if type_ == "schema":
        return name in (None, "public")
    return True


def include_object(obj, name, type_, reflected, compare_to) -> bool:
    """Delegate object filtering to GeoAlchemy2 (spatial indexes)."""
    if _object_schema(obj) not in (None, "public"):
        return False
    return alembic_helpers.include_object(obj, name, type_, reflected, compare_to)


def render_item(type_, obj, autogen_context) -> str:
    """Delegate rendering to GeoAlchemy2 (geometry types)."""
    return alembic_helpers.render_item(type_, obj, autogen_context)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        include_object=include_object,
        render_item=render_item,
        process_revision_directives=alembic_helpers.writer,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_name=include_name,
        include_object=include_object,
        render_item=render_item,
        process_revision_directives=alembic_helpers.writer,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with an async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
