"""Added themes table

Revision ID: a494c0e4fe77
Revises:
Create Date: 2020-03-01 07:55:21.366905

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a494c0e4fe77'
down_revision = 'e1470cd0df7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('themes',
    sa.Column('ID', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('resource_type', sa.Text(), nullable=False),
    sa.Column('slug', sa.Text(), nullable=True),
    sa.Column('theme', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_index('themes_idx', 'themes', ['resource_id', 'slug'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('themes_idx', table_name='themes')
    op.drop_table('themes')
    # ### end Alembic commands ###