"""create incident evidence review tables

Revision ID: 0006
Revises: 0005
Create Date: 2026-06-18
"""
from alembic import op
import sqlalchemy as sa

revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'violation_candidates',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('track_id', sa.String(64), sa.ForeignKey('tracks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('frame_id', sa.String(64), sa.ForeignKey('frames.id', ondelete='SET NULL'), nullable=True),
        sa.Column('violation_type', sa.String(100), nullable=False),
        sa.Column('confidence', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'incidents',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('track_id', sa.String(64), sa.ForeignKey('tracks.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='OPEN'),
        sa.Column('confidence_score', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'incident_scores',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('incident_id', sa.String(64), sa.ForeignKey('incidents.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('detection_score', sa.Float, server_default=sa.text('0.0')),
        sa.Column('tracking_score', sa.Float, server_default=sa.text('0.0')),
        sa.Column('anpr_score', sa.Float, server_default=sa.text('0.0')),
        sa.Column('rule_score', sa.Float, server_default=sa.text('0.0')),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'evidence_assets',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('incident_id', sa.String(64), sa.ForeignKey('incidents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('asset_type', sa.String(50), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'review_actions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('incident_id', sa.String(64), sa.ForeignKey('incidents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reviewer_id', sa.String(64), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('notes', sa.String(1000), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('review_actions')
    op.drop_table('evidence_assets')
    op.drop_table('incident_scores')
    op.drop_table('incidents')
    op.drop_table('violation_candidates')
