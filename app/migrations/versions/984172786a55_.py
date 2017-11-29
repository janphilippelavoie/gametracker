"""empty message

Revision ID: 984172786a55
Revises: f0b1122fdcb6
Create Date: 2017-11-29 22:19:06.357456

"""

# revision identifiers, used by Alembic.
revision = '984172786a55'
down_revision = 'f0b1122fdcb6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('played',
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('match_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('played')
    # ### end Alembic commands ###