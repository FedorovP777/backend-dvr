import os

from sqlalchemy import create_engine

db_url = os.environ.get('DB_URL', 'postgresql://dvr:dvr@localhost:5432/dvr')

engine = create_engine(db_url, echo=True, future=True)
