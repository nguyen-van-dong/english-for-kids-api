"""Dynamic CMS Schema for Curriculum, Games, Gamification, and CMS

Revision ID: 2026_09_11_0002
Revises: 2026_09_11_0001
Create Date: 2026-09-11 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2026_09_11_0002'
down_revision: Union[str, None] = '2026_09_11_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 0. Add is_admin to users
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # 1. Categories
    op.create_table(
        'categories',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(), nullable=False, server_default='paw'),
        sa.Column('color', sa.String(), nullable=False, server_default='#FF9671'),
        sa.Column('light_color', sa.String(), nullable=False, server_default='#FFF0EB'),
        sa.Column('age_min', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('age_max', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('is_free', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_order_index'), 'categories', ['order_index'], unique=False)
    op.create_index(op.f('ix_categories_is_active'), 'categories', ['is_active'], unique=False)

    # 2. Vocabulary Words
    op.create_table(
        'vocabulary_words',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('category_id', sa.String(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('phonetic', sa.String(), nullable=True),
        sa.Column('emoji', sa.String(), nullable=False, server_default='🌟'),
        sa.Column('meaning_vi', sa.String(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('custom_audio_url', sa.String(), nullable=True),
        sa.Column('example_sentence', sa.Text(), nullable=True),
        sa.Column('sentence_meaning_vi', sa.Text(), nullable=True),
        sa.Column('fun_fact', sa.Text(), nullable=True),
        sa.Column('difficulty_level', sa.String(), nullable=True, server_default='easy'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vocabulary_words_id'), 'vocabulary_words', ['id'], unique=False)
    op.create_index(op.f('ix_vocabulary_words_category_id'), 'vocabulary_words', ['category_id'], unique=False)
    op.create_index(op.f('ix_vocabulary_words_word'), 'vocabulary_words', ['word'], unique=False)
    op.create_index(op.f('ix_vocabulary_words_difficulty_level'), 'vocabulary_words', ['difficulty_level'], unique=False)
    op.create_index(op.f('ix_vocabulary_words_order_index'), 'vocabulary_words', ['order_index'], unique=False)
    op.create_index(op.f('ix_vocabulary_words_is_active'), 'vocabulary_words', ['is_active'], unique=False)

    # 3. Alphabet Lessons
    op.create_table(
        'alphabet_lessons',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('letter', sa.String(), nullable=False),
        sa.Column('lowercase', sa.String(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('phonics', sa.String(), nullable=False),
        sa.Column('emoji', sa.String(), nullable=False, server_default='🍎'),
        sa.Column('example_sentence', sa.Text(), nullable=True),
        sa.Column('color', sa.String(), nullable=False, server_default='#FF6B6B'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alphabet_lessons_id'), 'alphabet_lessons', ['id'], unique=False)
    op.create_index(op.f('ix_alphabet_lessons_letter'), 'alphabet_lessons', ['letter'], unique=False)
    op.create_index(op.f('ix_alphabet_lessons_order_index'), 'alphabet_lessons', ['order_index'], unique=False)
    op.create_index(op.f('ix_alphabet_lessons_is_active'), 'alphabet_lessons', ['is_active'], unique=False)

    # 4. Quiz Questions
    op.create_table(
        'quiz_questions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('category_id', sa.String(), nullable=True, server_default='general'),
        sa.Column('level', sa.String(), nullable=True, server_default='easy'),
        sa.Column('question_type', sa.String(), nullable=True, server_default='picture-word'),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('target_word', sa.String(), nullable=False),
        sa.Column('prompt_emoji', sa.String(), nullable=True, server_default='❓'),
        sa.Column('prompt_audio', sa.String(), nullable=True),
        sa.Column('prompt_image_url', sa.String(), nullable=True),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('reward_stars', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_questions_id'), 'quiz_questions', ['id'], unique=False)
    op.create_index(op.f('ix_quiz_questions_category_id'), 'quiz_questions', ['category_id'], unique=False)
    op.create_index(op.f('ix_quiz_questions_level'), 'quiz_questions', ['level'], unique=False)
    op.create_index(op.f('ix_quiz_questions_is_active'), 'quiz_questions', ['is_active'], unique=False)

    # 5. Spelling Words
    op.create_table(
        'spelling_words',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('word', sa.String(), nullable=False),
        sa.Column('emoji', sa.String(), nullable=False, server_default='✨'),
        sa.Column('hint', sa.String(), nullable=False),
        sa.Column('level', sa.String(), nullable=True, server_default='easy'),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('audio_url', sa.String(), nullable=True),
        sa.Column('reward_stars', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_spelling_words_id'), 'spelling_words', ['id'], unique=False)
    op.create_index(op.f('ix_spelling_words_word'), 'spelling_words', ['word'], unique=False)
    op.create_index(op.f('ix_spelling_words_level'), 'spelling_words', ['level'], unique=False)
    op.create_index(op.f('ix_spelling_words_is_active'), 'spelling_words', ['is_active'], unique=False)

    # 6. Speaking Challenges
    op.create_table(
        'speaking_challenges',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('phonetic', sa.String(), nullable=True),
        sa.Column('emoji', sa.String(), nullable=False, server_default='🗣️'),
        sa.Column('level', sa.String(), nullable=True, server_default='easy'),
        sa.Column('fun_fact', sa.Text(), nullable=True),
        sa.Column('pass_threshold_percent', sa.Integer(), nullable=True, server_default='70'),
        sa.Column('reward_stars', sa.Integer(), nullable=True, server_default='2'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_speaking_challenges_id'), 'speaking_challenges', ['id'], unique=False)
    op.create_index(op.f('ix_speaking_challenges_text'), 'speaking_challenges', ['text'], unique=False)
    op.create_index(op.f('ix_speaking_challenges_level'), 'speaking_challenges', ['level'], unique=False)
    op.create_index(op.f('ix_speaking_challenges_is_active'), 'speaking_challenges', ['is_active'], unique=False)

    # 7. Achievement Badges
    op.create_table(
        'achievements_badges',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('badge_icon', sa.String(), nullable=False, server_default='🏆'),
        sa.Column('badge_image_url', sa.String(), nullable=True),
        sa.Column('condition_type', sa.String(), nullable=False),
        sa.Column('condition_value', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('reward_stars', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_badges_id'), 'achievements_badges', ['id'], unique=False)
    op.create_index(op.f('ix_achievements_badges_condition_type'), 'achievements_badges', ['condition_type'], unique=False)
    op.create_index(op.f('ix_achievements_badges_is_active'), 'achievements_badges', ['is_active'], unique=False)

    # 8. Avatar Characters
    op.create_table(
        'avatars_characters',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('emoji', sa.String(), nullable=False, server_default='🦁'),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('unlock_type', sa.String(), nullable=True, server_default='free'),
        sa.Column('price_stars', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('required_level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_avatars_characters_id'), 'avatars_characters', ['id'], unique=False)
    op.create_index(op.f('ix_avatars_characters_unlock_type'), 'avatars_characters', ['unlock_type'], unique=False)
    op.create_index(op.f('ix_avatars_characters_is_active'), 'avatars_characters', ['is_active'], unique=False)

    # 9. Sticker Store
    op.create_table(
        'stickers_store',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('emoji', sa.String(), nullable=False, server_default='🚀'),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('category_name', sa.String(), nullable=True, server_default='General'),
        sa.Column('price_stars', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stickers_store_id'), 'stickers_store', ['id'], unique=False)
    op.create_index(op.f('ix_stickers_store_is_active'), 'stickers_store', ['is_active'], unique=False)

    # 10. Home Banners
    op.create_table(
        'home_banners',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('subtitle', sa.String(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('action_type', sa.String(), nullable=True, server_default='NAVIGATE_CATEGORY'),
        sa.Column('action_payload', sa.String(), nullable=True, server_default='animals'),
        sa.Column('background_color', sa.String(), nullable=True, server_default='#4D96FF'),
        sa.Column('display_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_home_banners_id'), 'home_banners', ['id'], unique=False)
    op.create_index(op.f('ix_home_banners_display_order'), 'home_banners', ['display_order'], unique=False)
    op.create_index(op.f('ix_home_banners_is_active'), 'home_banners', ['is_active'], unique=False)

    # 11. Daily Quests
    op.create_table(
        'daily_quests',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('emoji', sa.String(), nullable=True, server_default='🎯'),
        sa.Column('target_type', sa.String(), nullable=False),
        sa.Column('target_count', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('reward_stars', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('day_of_week', sa.Integer(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_quests_id'), 'daily_quests', ['id'], unique=False)
    op.create_index(op.f('ix_daily_quests_target_type'), 'daily_quests', ['target_type'], unique=False)
    op.create_index(op.f('ix_daily_quests_is_active'), 'daily_quests', ['is_active'], unique=False)

    # 12. App Settings
    op.create_table(
        'app_settings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('config_key', sa.String(), nullable=False),
        sa.Column('config_value', sa.Text(), nullable=False),
        sa.Column('data_type', sa.String(), nullable=True, server_default='string'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_settings_config_key'), 'app_settings', ['config_key'], unique=True)

    # 13. Content Versions
    op.create_table(
        'content_versions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_versions_id'), 'content_versions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('content_versions')
    op.drop_table('app_settings')
    op.drop_table('daily_quests')
    op.drop_table('home_banners')
    op.drop_table('stickers_store')
    op.drop_table('avatars_characters')
    op.drop_table('achievements_badges')
    op.drop_table('speaking_challenges')
    op.drop_table('spelling_words')
    op.drop_table('quiz_questions')
    op.drop_table('alphabet_lessons')
    op.drop_table('vocabulary_words')
    op.drop_table('categories')
    op.drop_column('users', 'is_admin')
