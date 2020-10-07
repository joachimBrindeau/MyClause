"""Added Clause model

Revision ID: 97f2330865a3
Revises: 4f704a7b5595
Create Date: 2020-10-06 20:15:49.682649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97f2330865a3'
down_revision = '4f704a7b5595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clause',
    sa.Column('clause_id', sa.Integer(), nullable=False),
    sa.Column('clause_title', sa.String(length=720), nullable=True),
    sa.Column('clause_text', sa.UnicodeText(), nullable=True),
    sa.Column('clause_full_text', sa.UnicodeText(), nullable=True),
    sa.Column('clause_user', sa.Integer(), nullable=True),
    sa.Column('clause_private', sa.Boolean(), nullable=True),
    sa.Column('clause_created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['clause_user'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('clause_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clause')
    # ### end Alembic commands ###
