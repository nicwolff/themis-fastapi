from datetime import datetime
from os import environ

import sqlalchemy as sa
from sqlalchemy import Column, DateTime, Index, Table, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

connect_str = 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**environ)
engine = sa.create_engine(connect_str)

metadata = sa.MetaData()
metadata.bind = engine

now = datetime.utcnow
new_uuid = sa.text('uuid_generate_v4()')

themes = Table(
    'themes',
    metadata,
    Column('ID', UUID(as_uuid=True), primary_key=True, server_default=new_uuid),
    Column('resource_id', UUID(as_uuid=True), nullable=False),
    Column('resource_type', Text, nullable=False),
    Column('slug', Text, nullable=True),
    Column('theme', JSONB, nullable=False),
    Column('created_at', DateTime, nullable=False, default=now),
    Column('updated_at', DateTime, nullable=False, default=now, onupdate=now),
    Index('themes_resource_id_idx', 'resource_id', unique=True),
    Index('themes_idx', 'resource_id', 'slug', unique=True),
)
