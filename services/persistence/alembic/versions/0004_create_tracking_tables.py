"""create tracking tables

Revision ID: 0004
Revises: 0003
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tracks',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('camera_id', sa.String(64), nullable=False),
        sa.Column('class_name', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('1')),
        sa.Column('first_seen_at', sa.DateTime, nullable=True),
        sa.Column('last_seen_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'track_history',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('track_id', sa.String(64), sa.ForeignKey('tracks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('frame_id', sa.String(64), sa.ForeignKey('frames.id', ondelete='SET NULL'), nullable=True),
        sa.Column('x', sa.Float, nullable=False),
        sa.Column('y', sa.Float, nullable=False),
        sa.Column('speed', sa.Float, nullable=True),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('track_history')
    op.drop_table('tracks')
