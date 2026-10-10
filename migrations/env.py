"""Alembic environment shared by CLI and application startup."""
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import make_url
from app.core.config import get_settings
from app.core.database import Base
import app.models.models  # noqa: F401

config = context.config
target_metadata = Base.metadata
connection = config.attributes.get("connection")
if connection is not None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
elif context.is_offline_mode():
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
else:
    raw_url = get_settings().database_url.strip()
    if raw_url.startswith("postgres://"):
        raw_url = "postgresql://" + raw_url[len("postgres://"):]
    url = make_url(raw_url)
    if url.drivername in ("postgresql+asyncpg", "postgresql", "postgres"):
        url = url.set(drivername="postgresql+psycopg")
    elif url.drivername == "sqlite+aiosqlite":
        url = url.set(drivername="sqlite")
    query = dict(url.query)
    if "channel_binding" in query:
        del query["channel_binding"]
        url = url.set(query=query)
    config.set_main_option("sqlalchemy.url", url.render_as_string(hide_password=False).replace("%", "%%"))
    engine = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
