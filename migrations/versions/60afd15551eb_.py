"""empty message

Revision ID: 60afd15551eb
Revises: afc2794b27b4
Create Date: 2024-09-29 18:13:18.039674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60afd15551eb'
down_revision = 'afc2794b27b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_gst', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.drop_column('is_gst')

    # ### end Alembic commands ###