"""empty message

Revision ID: 481cdebb1c41
Revises: 
Create Date: 2024-03-01 21:47:29.603939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '481cdebb1c41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('discount_percentage', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('discount_amount', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('total_amount', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('gst_amount', sa.Text(), nullable=True))
        batch_op.drop_column('invoice_parcel_details')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoices', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invoice_parcel_details', sa.TEXT(), nullable=True))
        batch_op.drop_column('gst_amount')
        batch_op.drop_column('total_amount')
        batch_op.drop_column('discount_amount')
        batch_op.drop_column('discount_percentage')

    # ### end Alembic commands ###