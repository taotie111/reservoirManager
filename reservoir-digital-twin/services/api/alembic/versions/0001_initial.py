from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'reservoirs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('geometry', sa.Text(), nullable=True),
        sa.Column('capacity_m3', sa.Float(), nullable=True),
        sa.Column('normal_level', sa.Float(), nullable=True),
        sa.Column('dead_level', sa.Float(), nullable=True),
    )

    op.create_table(
        'stations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('reservoir_id', sa.Integer(), sa.ForeignKey('reservoirs.id')), 
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=True),
        sa.Column('location', sa.Text(), nullable=True),
    )

    op.create_table(
        'sensors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('station_id', sa.Integer(), sa.ForeignKey('stations.id')), 
        sa.Column('sensor_type', sa.String(length=50), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=True),
    )

    op.create_table(
        'measurements',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sensor_id', sa.Integer(), sa.ForeignKey('sensors.id')),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('quality_flag', sa.String(length=20), nullable=True),
    )

    op.create_table(
        'forecasts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('reservoir_id', sa.Integer(), sa.ForeignKey('reservoirs.id')),
        sa.Column('forecast_data', sa.Text(), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
    )

    op.create_table(
        'schedules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('reservoir_id', sa.Integer(), sa.ForeignKey('reservoirs.id')),
        sa.Column('outflow_plan', sa.Text(), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=True),
    )

    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('reservoir_id', sa.Integer(), sa.ForeignKey('reservoirs.id')),
        sa.Column('alert_type', sa.String(length=50), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=True),
        sa.Column('payload', sa.Text(), nullable=True),
    )

    op.create_table(
        'materials',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100)),
        sa.Column('quantity', sa.Float()),
        sa.Column('location', sa.Text(), nullable=True),
    )

    op.create_table(
        'exercises',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100)),
        sa.Column('scenario', sa.Text(), nullable=True),
        sa.Column('results', sa.Text(), nullable=True),
    )

    op.create_table(
        'ml_models',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100)),
        sa.Column('version', sa.String(length=20)),
    )

def downgrade():
    op.drop_table('ml_models')
    op.drop_table('exercises')
    op.drop_table('materials')
    op.drop_table('alerts')
    op.drop_table('schedules')
    op.drop_table('forecasts')
    op.drop_table('measurements')
    op.drop_table('sensors')
    op.drop_table('stations')
    op.drop_table('reservoirs')
    op.drop_table('users')
