"""empty message

Revision ID: cd1b72a6000e
Revises: 9aac83ab3e14
Create Date: 2024-03-08 22:39:34.332732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd1b72a6000e'
down_revision = '9aac83ab3e14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.alter_column('invoice_date',
               existing_type=sa.DATETIME(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.alter_column('invoice_date',
               existing_type=sa.Text(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
