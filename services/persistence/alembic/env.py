import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the persistence service root to sys.path so models can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Base and all models so Alembic can detect them
from app.db.base import Base
from app.models.camera_models import Camera, CameraCalibration, CameraZone
from app.models.frame_models import Frame, FrameQualityMetric
from app.models.detection_models import Detection
from app.models.tracking_models import Track, TrackHistory
from app.models.anpr_models import PlateRead, PlateCandidateRecord
from app.models.incident_models import (
    ViolationCandidateRecord, Incident, IncidentScore, EvidenceAsset, ReviewAction
)

# Alembic Config object
config = context.config

# Set up loggers from the config file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Allow DB_URL env var to override alembic.ini
db_url = os.getenv("DB_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Target metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    Generates SQL scripts without requiring a live database connection.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    Creates an engine and associates a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
