"""add place table, relationship with event

Revision ID: 296effb09a76
Revises: 127959d37051
Create Date: 2022-04-09 00:28:46.050931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '296effb09a76'
down_revision = '127959d37051'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('place',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=15), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_place_id'), 'place', ['id'], unique=False)
    op.add_column('event', sa.Column('place_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'place', ['place_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'place_id')
    op.drop_index(op.f('ix_place_id'), table_name='place')
    op.drop_table('place')
    # ### end Alembic commands ###
