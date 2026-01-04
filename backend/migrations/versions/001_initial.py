"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_is_deleted'), 'users', ['is_deleted'], unique=False)
    
    # Create daily_entries table
    op.create_table(
        'daily_entries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('income', sa.Float(), nullable=False),
        sa.Column('income_description', sa.Text(), nullable=True),
        sa.Column('expense', sa.Float(), nullable=False),
        sa.Column('expense_category', sa.Enum('FOOD', 'TRANSPORT', 'ENTERTAINMENT', 'HOUSING', 'UTILITIES', 'HEALTHCARE', 'EDUCATION', 'SHOPPING', 'SUBSCRIPTIONS', 'OTHER', name='expensecategory'), nullable=True),
        sa.Column('expense_description', sa.Text(), nullable=True),
        sa.Column('gold_grams', sa.Float(), nullable=False),
        sa.Column('silver_grams', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_entries_user_id'), 'daily_entries', ['user_id'], unique=False)
    op.create_index(op.f('ix_daily_entries_date'), 'daily_entries', ['date'], unique=False)
    op.create_index(op.f('ix_daily_entries_is_deleted'), 'daily_entries', ['is_deleted'], unique=False)
    
    # Create investments table
    op.create_table(
        'investments',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('investment_type', sa.Enum('GOLD', 'SILVER', 'STOCKS', 'BONDS', 'CRYPTO', 'ETF', 'REAL_ESTATE', 'SAVINGS', 'OTHER', name='investmenttype'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=True),
        sa.Column('purchase_date', sa.Date(), nullable=False),
        sa.Column('current_value', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investments_user_id'), 'investments', ['user_id'], unique=False)
    op.create_index(op.f('ix_investments_investment_type'), 'investments', ['investment_type'], unique=False)
    op.create_index(op.f('ix_investments_purchase_date'), 'investments', ['purchase_date'], unique=False)
    op.create_index(op.f('ix_investments_is_deleted'), 'investments', ['is_deleted'], unique=False)
    
    # Create monthly_goals table
    op.create_table(
        'monthly_goals',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('income_goal', sa.Float(), nullable=False),
        sa.Column('gold_goal', sa.Float(), nullable=False),
        sa.Column('silver_goal', sa.Float(), nullable=False),
        sa.Column('investment_goal', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_monthly_goals_user_id'), 'monthly_goals', ['user_id'], unique=False)
    op.create_index(op.f('ix_monthly_goals_year'), 'monthly_goals', ['year'], unique=False)
    op.create_index(op.f('ix_monthly_goals_month'), 'monthly_goals', ['month'], unique=False)
    op.create_index(op.f('ix_monthly_goals_is_deleted'), 'monthly_goals', ['is_deleted'], unique=False)
    
    # Create notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
    op.create_index(op.f('ix_notifications_is_read'), 'notifications', ['is_read'], unique=False)
    op.create_index(op.f('ix_notifications_is_deleted'), 'notifications', ['is_deleted'], unique=False)


def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('monthly_goals')
    op.drop_table('investments')
    op.drop_table('daily_entries')
    op.drop_table('users')
