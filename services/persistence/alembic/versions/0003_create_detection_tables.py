"""create detection tables

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'detections',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('frame_id', sa.String(64), sa.ForeignKey('frames.id', ondelete='CASCADE'), nullable=False),
        sa.Column('class_name', sa.String(100), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False),
        sa.Column('bbox_x1', sa.Float, nullable=False),
        sa.Column('bbox_y1', sa.Float, nullable=False),
        sa.Column('bbox_x2', sa.Float, nullable=False),
        sa.Column('bbox_y2', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('detections')
