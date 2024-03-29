""" Database module """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set as module level constants
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
TASKTRACKER_DB_NAME = os.environ.get('TASKTRACKER_DB_NAME')
TASKTRACKER_DB_CONNECTION_STRING = os.environ.get('TASKTRACKER_DB_CONNECTION_STRING')
IS_ACC_ENVIRONMENT = os.environ.get('ENVIRONMENT') == "ACC"

print("DB_USER: ", DB_USER)
print("DB_PASSWORD: ", DB_PASSWORD)
print("DB_HOST: ", DB_HOST)
print("TASKTRACKER_DB_NAME: ", TASKTRACKER_DB_NAME)
print("TASKTRACKER_DB_CONNECTION_STRING: ", TASKTRACKER_DB_CONNECTION_STRING)

def create_database_session():
    """ Create and return a database session """
    echo_log = bool(IS_ACC_ENVIRONMENT)
    engine = create_engine(
        TASKTRACKER_DB_CONNECTION_STRING,
        echo=echo_log
    )
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = create_database_session()

Base = declarative_base()
