"""partitioning

Revision ID: a45604cd7586
Revises: 2f7ea957b2c3
Create Date: 2022-12-07 00:12:50.950062

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a45604cd7586'
down_revision = '2f7ea957b2c3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('auth_history')
    op.create_table('auth_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('logged_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_device_type', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'user_device_type'),
    sa.UniqueConstraint('id', 'user_device_type'),
    postgresql_partition_by='LIST (user_device_type)'
    )
    op.execute("""CREATE TABLE IF NOT EXISTS "auth_history_smart" PARTITION OF "auth_history" FOR VALUES IN ('smart')""")
    op.execute("""CREATE TABLE IF NOT EXISTS "auth_history_mobile" PARTITION OF "auth_history" FOR VALUES IN ('mobile')""")
    op.execute("""CREATE TABLE IF NOT EXISTS "auth_history_web" PARTITION OF "auth_history" FOR VALUES IN ('web')""")
    op.execute("""CREATE TABLE IF NOT EXISTS "auth_history_other" PARTITION OF "auth_history" FOR VALUES IN ('other')""")


def downgrade():
    op.drop_table('auth_history')
    op.create_table('auth_history',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('user', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_agent', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('logged_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], name='auth_history_user_fkey'),
    sa.PrimaryKeyConstraint('id', name='auth_history_pkey')
    )
