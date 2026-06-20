"""create camera tables

Revision ID: 0001
Revises: 
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cameras',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('latitude', sa.Float, nullable=True),
        sa.Column('longitude', sa.Float, nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='ONLINE'),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'camera_calibrations',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('camera_id', sa.String(64), sa.ForeignKey('cameras.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('intrinsic_matrix', sa.String(500), nullable=True),
        sa.Column('distortion_coeffs', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'camera_zones',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('camera_id', sa.String(64), sa.ForeignKey('cameras.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('zone_type', sa.String(100), nullable=False),
        sa.Column('polygon', sa.String(1000), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('camera_zones')
    op.drop_table('camera_calibrations')
    op.drop_table('cameras')
