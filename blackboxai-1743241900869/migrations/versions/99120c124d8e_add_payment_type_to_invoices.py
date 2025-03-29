"""add payment_type to invoices

Revision ID: 99120c124d8e
Revises: 1ebad9aa9bfe
Create Date: 2025-03-29 20:12:45.079170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99120c124d8e'
down_revision = '1ebad9aa9bfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payment_type', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invoice', schema=None) as batch_op:
        batch_op.drop_column('payment_type')

    # ### end Alembic commands ###
