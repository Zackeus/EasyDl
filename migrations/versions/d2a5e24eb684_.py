"""empty message

Revision ID: d2a5e24eb684
Revises: 
Create Date: 2019-04-28 10:34:33.596738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2a5e24eb684'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('LOAN_IMG_DETAIL', sa.Column('OCR_INFO', sa.String(), nullable=True, comment='OCR识别信息'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('LOAN_IMG_DETAIL', 'OCR_INFO')
    # ### end Alembic commands ###
