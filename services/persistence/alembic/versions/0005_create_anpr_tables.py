"""create anpr tables

Revision ID: 0005
Revises: 0004
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'plate_reads',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('frame_id', sa.String(64), sa.ForeignKey('frames.id', ondelete='CASCADE'), nullable=False),
        sa.Column('track_id', sa.String(64), sa.ForeignKey('tracks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('best_plate_text', sa.String(50), nullable=False),
        sa.Column('best_confidence', sa.Float, nullable=False),
        sa.Column('region', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'plate_candidates',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('plate_read_id', sa.String(64), sa.ForeignKey('plate_reads.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plate_text', sa.String(50), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('plate_candidates')
    op.drop_table('plate_reads')
