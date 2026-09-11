"""Initial database schema with users, study_sessions, timeline_events, and word_progress

Revision ID: 2026_09_11_0001
Revises: 
Create Date: 2026-09-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2026_09_11_0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('parent_name', sa.String(), nullable=True, server_default=''),
        sa.Column('child_name', sa.String(), nullable=False, server_default='Little Explorer'),
        sa.Column('child_age', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('avatar', sa.String(), nullable=False, server_default='🦁'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('verification_code', sa.String(), nullable=True),
        sa.Column('verification_code_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('stars', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('streak_days', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('last_active_date', sa.String(), nullable=True, server_default=''),
        sa.Column('mastered_words', sa.JSON(), nullable=True),
        sa.Column('completed_categories', sa.JSON(), nullable=True),
        sa.Column('quiz_high_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_study_minutes', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # 2. Create study_sessions table
    op.create_table(
        'study_sessions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.String(), nullable=False),
        sa.Column('ended_at', sa.String(), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('activities_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_study_sessions_id'), 'study_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_study_sessions_user_id'), 'study_sessions', ['user_id'], unique=False)

    # 3. Create timeline_events table
    op.create_table(
        'timeline_events',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('target_word', sa.String(), nullable=True),
        sa.Column('category_title', sa.String(), nullable=True),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('stars_earned', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_correct', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('timestamp', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_timeline_events_id'), 'timeline_events', ['id'], unique=False)
    op.create_index(op.f('ix_timeline_events_user_id'), 'timeline_events', ['user_id'], unique=False)
    op.create_index(op.f('ix_timeline_events_event_type'), 'timeline_events', ['event_type'], unique=False)

    # 4. Create word_progress table
    op.create_table(
        'word_progress',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('word_id', sa.String(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('category_id', sa.String(), nullable=True, server_default='general'),
        sa.Column('status', sa.String(), nullable=True, server_default='learning'),
        sa.Column('accuracy_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('attempts_count', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('last_practiced_at', sa.String(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_word_progress_id'), 'word_progress', ['id'], unique=False)
    op.create_index(op.f('ix_word_progress_user_id'), 'word_progress', ['user_id'], unique=False)
    op.create_index(op.f('ix_word_progress_word_id'), 'word_progress', ['word_id'], unique=False)


def downgrade() -> None:
    op.drop_table('word_progress')
    op.drop_table('timeline_events')
    op.drop_table('study_sessions')
    op.drop_table('users')
