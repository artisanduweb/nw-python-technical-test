"""Update Group model relationships

Revision ID: b81b30093d1e
Revises: 93e1910e0b81
Create Date: 2024-05-25 18:21:40.070373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b81b30093d1e'
down_revision: Union[str, None] = '93e1910e0b81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('group1', 'group2', 'group3', name='grouptype'), nullable=False),
    sa.Column('parent_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_id'), 'groups', ['id'], unique=False)
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=True)
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('installation_date', sa.Date(), nullable=True),
    sa.Column('max_power_megawatt', sa.Float(), nullable=True),
    sa.Column('min_power_megawatt', sa.Float(), nullable=True),
    sa.Column('useful_energy_at_1_megawatt', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sites_id'), 'sites', ['id'], unique=False)
    op.create_index(op.f('ix_sites_name'), 'sites', ['name'], unique=False)
    op.create_table('site_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
    sa.PrimaryKeyConstraint('id', 'site_id', 'group_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('site_group')
    op.drop_index(op.f('ix_sites_name'), table_name='sites')
    op.drop_index(op.f('ix_sites_id'), table_name='sites')
    op.drop_table('sites')
    op.drop_index(op.f('ix_groups_name'), table_name='groups')
    op.drop_index(op.f('ix_groups_id'), table_name='groups')
    op.drop_table('groups')
    # ### end Alembic commands ###