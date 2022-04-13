"""add table user_organization

Revision ID: d89a16e88480
Revises: b4cdfb0e3619
Create Date: 2022-04-13 19:11:48.274770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd89a16e88480'
down_revision = 'b4cdfb0e3619'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userorganization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('organization_id', 'user_id', name='unique_user_organization')
    )
    op.create_index(op.f('ix_userorganization_id'), 'userorganization', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_userorganization_id'), table_name='userorganization')
    op.drop_table('userorganization')
    # ### end Alembic commands ###
