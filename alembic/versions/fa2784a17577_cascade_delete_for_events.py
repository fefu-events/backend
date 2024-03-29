"""cascade delete for events

Revision ID: fa2784a17577
Revises: 17c88d299129
Create Date: 2022-04-09 17:40:10.348984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa2784a17577'
down_revision = '17c88d299129'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('event_place_id_fkey', 'event', type_='foreignkey')
    op.drop_constraint('event_user_id_fkey', 'event', type_='foreignkey')
    op.drop_constraint('event_category_id_fkey', 'event', type_='foreignkey')
    op.create_foreign_key(None, 'event', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'event', 'place', ['place_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'event', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.create_foreign_key('event_category_id_fkey', 'event', 'category', ['category_id'], ['id'])
    op.create_foreign_key('event_user_id_fkey', 'event', 'user', ['user_id'], ['id'])
    op.create_foreign_key('event_place_id_fkey', 'event', 'place', ['place_id'], ['id'])
    # ### end Alembic commands ###
