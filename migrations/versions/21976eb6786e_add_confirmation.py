"""add confirmation

Revision ID: 21976eb6786e
Revises: 74eb651b060a
Create Date: 2020-04-06 10:15:42.033861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21976eb6786e'
down_revision = '74eb651b060a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
