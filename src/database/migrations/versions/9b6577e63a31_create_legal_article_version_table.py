"""create_legal_article_version_table

Revision ID: 9b6577e63a31
Revises: 
Create Date: 2026-07-07 11:13:51.225994

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9b6577e63a31'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create legal_article_version table with indexes and exclusion constraints."""
    # 1. Enable btree_gist extension to support GiST exclusion constraint on scalar and range types
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    # 2. Create the table
    op.create_table(
        'legal_article_version',
        sa.Column('version_id', sa.String(length=50), nullable=False),
        sa.Column('article_id', sa.String(length=100), nullable=False),
        sa.Column('code_id', sa.String(length=50), nullable=False),
        sa.Column('article_number', sa.String(length=50), nullable=False),
        sa.Column('hierarchy_path', sa.Text(), nullable=False),
        sa.Column('text_ar', sa.Text(), nullable=False),
        sa.Column('text_fr', sa.Text(), nullable=True),
        sa.Column('valid_from', sa.Date(), nullable=False),
        sa.Column('valid_to', sa.Date(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='active'),
        sa.Column('source_ref', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_by_op', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('version_id')
    )

    # 3. Create indexes
    op.create_index('ix_legal_article_version_article_id', 'legal_article_version', ['article_id'])
    op.create_index('ix_legal_article_version_code_id', 'legal_article_version', ['code_id'])
    
    # Composite index to query by code, article number and date context efficiently
    op.create_index(
        'ix_legal_article_version_code_num_date',
        'legal_article_version',
        ['code_id', 'article_number', 'valid_from']
    )

    # 4. Add the GiST exclusion constraint to prevent overlapping temporal windows for the same article_id  # noqa: E501
    op.execute(
        "ALTER TABLE legal_article_version ADD CONSTRAINT exclude_overlapping_versions "
        "EXCLUDE USING gist (article_id WITH =, daterange(valid_from, valid_to, '[)') WITH &&)"
    )


def downgrade() -> None:
    """Downgrade schema: Drop table, constraints and indexes."""
    op.execute("ALTER TABLE legal_article_version DROP CONSTRAINT IF EXISTS exclude_overlapping_versions")  # noqa: E501
    op.drop_index('ix_legal_article_version_code_num_date')
    op.drop_index('ix_legal_article_version_code_id')
    op.drop_index('ix_legal_article_version_article_id')
    op.drop_table('legal_article_version')
