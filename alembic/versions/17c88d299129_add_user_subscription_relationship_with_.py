"""add user_subscription, relationship with user

Revision ID: 17c88d299129
Revises: 4e9bc6b1ed66
Create Date: 2022-04-09 16:23:50.804584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17c88d299129'
down_revision = '4e9bc6b1ed66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usersubscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usersubscription_id'), 'usersubscription', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usersubscription_id'), table_name='usersubscription')
    op.drop_table('usersubscription')
    # ### end Alembic commands ###