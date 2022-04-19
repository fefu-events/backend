"""delete tags organizations

Revision ID: c76de7afa966
Revises: 94fedb533740
Create Date: 2022-04-18 19:38:53.924571

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c76de7afa966'
down_revision = '94fedb533740'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('organization', 'tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organization', sa.Column('tags', postgresql.ARRAY(sa.VARCHAR(length=15)), server_default=sa.text("'{}'::character varying[]"), autoincrement=False, nullable=True))
    # ### end Alembic commands ###