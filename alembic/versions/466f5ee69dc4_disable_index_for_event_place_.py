"""disable index for event.place_description

Revision ID: 466f5ee69dc4
Revises: aa1826abe1cc
Create Date: 2022-04-05 16:23:59.314720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '466f5ee69dc4'
down_revision = 'aa1826abe1cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_event_place_description', table_name='event')
    op.create_unique_constraint(None, 'event', ['place_description'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='unique')
    op.create_index('ix_event_place_description', 'event', ['place_description'], unique=False)
    # ### end Alembic commands ###
