"""empty message

Revision ID: 391427c0fe94
Revises: 979e8fca5d8d
Create Date: 2021-07-05 16:43:57.646868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '391427c0fe94'
down_revision = '979e8fca5d8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'author_first')
    op.drop_column('books', 'author_last')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author_last', sa.VARCHAR(), nullable=True))
    op.add_column('books', sa.Column('author_first', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###