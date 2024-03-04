"""Creates a connection to the database and a session maker."""

from os import environ

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = environ["DB_USER"]
DB_PASSWORD = environ["DB_PASSWORD"]
DB_HOST = environ["DB_HOST"]
DB_NAME = environ["DB_NAME"]

url = URL.create("mysql+pymysql", DB_USER, DB_PASSWORD, DB_HOST, database=DB_NAME)
engine = create_engine(url, pool_size=10, max_overflow=20)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
