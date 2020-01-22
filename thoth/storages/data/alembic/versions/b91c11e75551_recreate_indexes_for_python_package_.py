"""Recreate indexes for Python package version

Revision ID: b91c11e75551
Revises: 1fbd52a03c73
Create Date: 2020-01-13 21:37:05.476084+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b91c11e75551'
down_revision = '1fbd52a03c73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('python_package_version_index_idx_00', 'python_package_version', ['package_name', 'package_version'], unique=False)
    op.drop_index('python_package_version_index_idx_10', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_10', 'python_package_version', ['package_name', 'package_version', 'os_name'], unique=False)
    op.drop_index('python_package_version_index_idx_11', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_11', 'python_package_version', ['package_name', 'package_version', 'os_version'], unique=False)
    op.drop_index('python_package_version_index_idx_12', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_12', 'python_package_version', ['package_name', 'package_version', 'python_version'], unique=False)
    op.drop_index('python_package_version_index_idx_20', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_20', 'python_package_version', ['package_name', 'package_version', 'os_name', 'os_version'], unique=False)
    op.drop_index('python_package_version_index_idx_21', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_21', 'python_package_version', ['package_name', 'package_version', 'os_name', 'python_version'], unique=False)
    op.drop_index('python_package_version_index_idx_22', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_22', 'python_package_version', ['package_name', 'package_version', 'os_version', 'python_version'], unique=False)
    op.drop_index('python_package_version_index_idx_30', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_30', 'python_package_version', ['package_name', 'package_version', 'os_name', 'os_version', 'python_version'], unique=False)
    op.drop_index('python_package_version_idx', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_13', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_23', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_24', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_25', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_31', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_32', table_name='python_package_version')
    op.drop_index('python_package_version_index_idx_33', table_name='python_package_version')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('python_package_version_index_idx_33', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'os_name', 'os_version', 'python_version'], unique=False)
    op.create_index('python_package_version_index_idx_32', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id', 'os_version', 'python_version'], unique=False)
    op.create_index('python_package_version_index_idx_31', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id', 'os_name', 'python_version'], unique=False)
    op.create_index('python_package_version_index_idx_25', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'os_version', 'python_version'], unique=False)
    op.create_index('python_package_version_index_idx_24', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'os_name', 'python_version'], unique=False)
    op.create_index('python_package_version_index_idx_23', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'os_name', 'os_version'], unique=False)
    op.create_index('python_package_version_index_idx_13', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_version'], unique=False)
    op.create_index('python_package_version_idx', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id'], unique=False)
    op.drop_index('python_package_version_index_idx_30', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_30', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id', 'os_name', 'os_version'], unique=False)
    op.drop_index('python_package_version_index_idx_22', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_22', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id', 'python_version'], unique=False)
    op.drop_index('python_package_version_index_idx_21', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_21', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id', 'os_version'], unique=False)
    op.drop_index('python_package_version_index_idx_20', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_20', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id', 'os_name'], unique=False)
    op.drop_index('python_package_version_index_idx_12', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_12', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'os_version'], unique=False)
    op.drop_index('python_package_version_index_idx_11', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_11', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'os_name'], unique=False)
    op.drop_index('python_package_version_index_idx_10', table_name='python_package_version')
    op.create_index('python_package_version_index_idx_10', 'python_package_version', ['package_name', 'package_version', 'python_package_index_id', 'python_package_index_id'], unique=False)
    op.drop_index('python_package_version_index_idx_00', table_name='python_package_version')
    # ### end Alembic commands ###
