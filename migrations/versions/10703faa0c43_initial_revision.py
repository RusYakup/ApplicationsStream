"""create applications table

Revision ID: a6b2d65a6e7f
Revises:
Create Date: 2023-10-20 15:23:34.302121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6b2d65a6e7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создаем таблицу applications
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_name', sa.String(25), nullable=False),
        sa.Column('description', sa.String(255)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()))


def downgrade():
    # Удаляем таблицу applications
    op.drop_table('applications')