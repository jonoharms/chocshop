"""numeric

Revision ID: 82721f470fb2
Revises: 1655085d07fe
Create Date: 2020-04-20 11:22:55.511751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82721f470fb2'
down_revision = '1655085d07fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'balance',
               existing_type=sa.NUMERIC(),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'balance',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
    # ### end Alembic commands ###
