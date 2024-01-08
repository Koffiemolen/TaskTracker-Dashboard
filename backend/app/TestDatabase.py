from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve the connection string from environment variables
automate_db_connection_string = os.getenv('AUTOMATE_DB_CONNECTION_STRING')
tasktracker_db_connection_string = os.getenv('TASKTRACKER_DB_CONNECTION_STRING')

# Test connection to TaskTracker DB
engine = create_engine(tasktracker_db_connection_string)
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Successfully connected to TaskTracker DB!")
except Exception as e:
    print(f"An error occurred while trying to connect to the TaskTracker DB: {e}")
