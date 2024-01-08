import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

username = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
server = os.environ.get('DB_HOST')
database = os.environ.get('TASKTRACKER_DB_NAME')
database_connection_string = os.environ.get('TASKTRACKER_DB_CONNECTION_STRING')

SQLALCHEMY_DATABASE_URL = database_connection_string

echo = True if os.environ.get('ENVIRONMENT') == "ACC" else False
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=echo
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
