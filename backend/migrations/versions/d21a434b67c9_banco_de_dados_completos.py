"""Banco de Dados Completos

Revision ID: d21a434b67c9
Revises: 
Create Date: 2025-04-01 11:15:19.908626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd21a434b67c9'
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
    op.create_table('procedure',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('time_service', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('profile', sa.Enum('CLIENT', 'ADMIN', name='profile_enum'), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    op.create_table('client',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('register_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('password_reset',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_cpf', sa.String(), nullable=False),
    sa.Column('token', sa.Text(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('used', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_cpf'], ['users.cpf'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
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
    sa.Column('procedure_id', sa.Integer(), nullable=False),
    sa.Column('date_appoint', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['pet_id'], ['pet.id'], ),
    sa.ForeignKeyConstraint(['procedure_id'], ['procedure.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointment')
    op.drop_table('pet')
    op.drop_table('contact')
    op.drop_table('address')
    op.drop_table('password_reset')
    op.drop_table('client')
    op.drop_table('users')
    op.drop_table('procedure')
    op.drop_table('breed')
    # ### end Alembic commands ###
