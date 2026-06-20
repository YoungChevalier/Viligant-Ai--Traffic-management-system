"""create frame tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'frames',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('camera_id', sa.String(64), sa.ForeignKey('cameras.id', ondelete='CASCADE'), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('processed', sa.Boolean, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'frame_quality_metrics',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('frame_id', sa.String(64), sa.ForeignKey('frames.id', ondelete='CASCADE'), nullable=False),
        sa.Column('metric_name', sa.String(100), nullable=False),
        sa.Column('metric_value', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('frame_quality_metrics')
    op.drop_table('frames')
