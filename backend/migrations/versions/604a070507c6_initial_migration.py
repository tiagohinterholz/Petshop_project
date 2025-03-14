"""Initial migration

Revision ID: 604a070507c6
Revises: 
Create Date: 2025-03-13 20:56:29.340991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '604a070507c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('breed',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description')
    )
    op.create_table('users',
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('profile', sa.Enum('CLIENT', 'ADMIN', name='profile_enum'), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('cpf'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('register_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['cpf'], ['users.cpf'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('neighborhood', sa.String(length=50), nullable=False),
    sa.Column('complement', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('type_contact', sa.Enum('telefone', 'email', name='contact_type_enum'), nullable=False),
    sa.Column('value_contact', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pet',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('breed_id', sa.Integer(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['breed_id'], ['breed.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('appointment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pet_id', sa.Integer(), nullable=False),
    sa.Column('desc_appoint', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('date_appoint', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['pet_id'], ['pet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment')
    op.drop_table('pet')
    op.drop_table('contact')
    op.drop_table('address')
    op.drop_table('client')
    op.drop_table('users')
    op.drop_table('breed')
    # ### end Alembic commands ###
