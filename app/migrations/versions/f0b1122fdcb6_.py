"""empty message

Revision ID: f0b1122fdcb6
Revises: f2462706170e
Create Date: 2017-11-29 21:58:00.331995

"""

# revision identifiers, used by Alembic.
revision = 'f0b1122fdcb6'
down_revision = 'f2462706170e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('matches')
    # ### end Alembic commands ###