"""Create index for get_depends_query.

Revision ID: 79e1d320db3d
Revises: 8231fee9a210
Create Date: 2019-11-29 16:59:44.869319+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e1d320db3d'
down_revision = '8231fee9a210'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('depends_on_version_id_idx', 'depends_on', ['version_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('depends_on_version_id_idx', table_name='depends_on')
    # ### end Alembic commands ###