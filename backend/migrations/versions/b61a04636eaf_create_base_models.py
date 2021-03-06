"""create base models

Revision ID: b61a04636eaf
Revises: 
Create Date: 2017-08-02 23:48:39.884208

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b61a04636eaf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('places',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image_urls', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('superplace_id', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['superplace_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_places_name'), 'places', ['name'], unique=True)
    op.create_table('plants',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('primary_name', sa.String(), nullable=False),
    sa.Column('common_names', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('scientific_names', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('substrates', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('plant_type', sa.String(), nullable=True),
    sa.Column('seed_image_urls', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('flower_image_urls', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('leaf_image_urls', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('other_image_urls', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('months_available', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plants_primary_name'), 'plants', ['primary_name'], unique=True)
    op.create_table('users',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('_password', sa.Binary(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plant_place',
    sa.Column('plant_id', postgresql.UUID(), nullable=True),
    sa.Column('place_id', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plant_place')
    op.drop_table('users')
    op.drop_index(op.f('ix_plants_primary_name'), table_name='plants')
    op.drop_table('plants')
    op.drop_index(op.f('ix_places_name'), table_name='places')
    op.drop_table('places')
    # ### end Alembic commands ###
