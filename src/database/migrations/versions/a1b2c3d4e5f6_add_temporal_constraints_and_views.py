"""add_temporal_constraints_and_views

Revision ID: a1b2c3d4e5f6
Revises: 9b6577e63a31
Create Date: 2026-07-08 07:45:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '9b6577e63a31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable btree_gist extension for ExcludeConstraint
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")

    # 2. Add indexes and constraints
    op.create_index('idx_article_valid', 'legal_article_version', ['article_id', 'valid_from'], unique=False)
    op.create_index('idx_code_article_valid', 'legal_article_version', ['code_id', 'article_number', 'valid_from'], unique=False)
    op.create_index('idx_source_ref', 'legal_article_version', ['source_ref'], unique=False, postgresql_using='gin')
    
    op.execute("""
        ALTER TABLE legal_article_version
        ADD CONSTRAINT excl_article_valid_dates
        EXCLUDE USING gist (
            article_id WITH =,
            daterange(valid_from, valid_to) WITH &&
        );
    """)

    # 3. Create views
    op.execute("""
        CREATE OR REPLACE VIEW current_article_versions AS
        SELECT *
        FROM legal_article_version
        WHERE CURRENT_DATE >= valid_from AND CURRENT_DATE < valid_to
        AND status = 'active';
    """)

    op.execute("""
        CREATE OR REPLACE VIEW article_versions_by_date AS
        SELECT *
        FROM legal_article_version
        ORDER BY article_id, valid_from DESC;
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS article_versions_by_date;")
    op.execute("DROP VIEW IF EXISTS current_article_versions;")
    
    op.execute("ALTER TABLE legal_article_version DROP CONSTRAINT IF EXISTS excl_article_valid_dates;")
    op.drop_index('idx_source_ref', table_name='legal_article_version', postgresql_using='gin')
    op.drop_index('idx_code_article_valid', table_name='legal_article_version')
    op.drop_index('idx_article_valid', table_name='legal_article_version')
