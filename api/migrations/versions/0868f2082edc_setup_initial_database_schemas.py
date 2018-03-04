"""Setup initial database schemas

Revision ID: 0868f2082edc
Revises: 
Create Date: 2018-03-03 00:42:15.148608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0868f2082edc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'address_book',
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('email', sa.String(254), unique=True),
        sa.Column('name', sa.String(64))
    )
    op.create_index(
        'ix_address_book_email',
        'address_book',
        ['email']
    )
    op.create_index(
        'ix_address_book_name',
        'address_book',
        ['name']
    )


def downgrade():
    op.drop_index('ix_address_book_email')
    op.drop_index('ix_address_book_name')
    op.drop_table('address_book')
