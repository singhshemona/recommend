"""empty message

Revision ID: 8cd4caa1a077
Revises: c99b0d3b05f2
Create Date: 2021-08-16 15:26:47.688651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cd4caa1a077'
down_revision = 'c99b0d3b05f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hundred_categories_ddc', sa.Column('tens_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'hundred_categories_ddc', 'ten_categories_ddc', ['tens_id'], ['id'])
    op.add_column('thousand_categories_ddc', sa.Column('hundreds_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'thousand_categories_ddc', 'hundred_categories_ddc', ['hundreds_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'thousand_categories_ddc', type_='foreignkey')
    op.drop_column('thousand_categories_ddc', 'hundreds_id')
    op.drop_constraint(None, 'hundred_categories_ddc', type_='foreignkey')
    op.drop_column('hundred_categories_ddc', 'tens_id')
    # ### end Alembic commands ###
