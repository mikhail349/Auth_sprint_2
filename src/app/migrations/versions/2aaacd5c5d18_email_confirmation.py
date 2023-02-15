"""email_confirmation

Revision ID: 2aaacd5c5d18
Revises: e953173b561e
Create Date: 2023-02-15 21:45:34.299765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aaacd5c5d18'
down_revision = 'e953173b561e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('auth_history', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('is_confirmed', sa.Boolean(), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('is_confirmed')
        batch_op.drop_column('email')

    with op.batch_alter_table('auth_history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
