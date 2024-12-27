import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="strongpwd",
    host=os.getenv("DB_HOST", default="localhost"),
    database=os.getenv("POSTGRES_DB", default="testdb"),
    port=int(os.getenv("DB_PORT", default=5433))
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)

def get_session():
    with Session() as session:
        yield session