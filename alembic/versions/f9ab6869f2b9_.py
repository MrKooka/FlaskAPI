"""empty message

Revision ID: f9ab6869f2b9
Revises: 
Create Date: 2021-05-07 14:02:07.199545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ab6869f2b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'videos', 'userapi', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'videos', type_='foreignkey')
    op.drop_column('videos', 'user_id')
    # ### end Alembic commands ###
