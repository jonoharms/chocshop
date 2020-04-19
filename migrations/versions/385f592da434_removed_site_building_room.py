"""removed site, building room

Revision ID: 385f592da434
Revises: fbc1c07d8e03
Create Date: 2020-04-20 09:45:50.843265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '385f592da434'
down_revision = 'fbc1c07d8e03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'building')
    op.drop_column('users', 'room')
    op.drop_column('users', 'site')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('site', sa.VARCHAR(length=64), nullable=True))
    op.add_column('users', sa.Column('room', sa.VARCHAR(length=64), nullable=True))
    op.add_column('users', sa.Column('building', sa.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###
