""" This module contains the DatabaseService class, which is a service for
managing and interacting with the database. """
import os
from sqlmodel import SQLModel, create_engine, Session, select
from backend.app.models.workflow_link_construct import WorkflowLinkConstruct  # pylint: disable=import-error

DATABASE_URL = os.getenv('AUTOMATE_DB_CONNECTION_STRING')
# Create an engine instance
engine = create_engine(DATABASE_URL, echo=True)

class DatabaseService:
    """
    A service for managing and interacting with the database.
    """

    @classmethod
    def create_tables(cls):
        """
        This method creates all tables based on the SQLModel metadata.
        Note: For production systems, you might manage database migrations with Alembic instead.
        """
        with engine.begin() as conn:
            # Note: SQLModel.metadata.create_all is a synchronous operation.
            SQLModel.metadata.create_all(conn)

    @classmethod
    def fetch_workflow_link_constructs(cls) -> list[WorkflowLinkConstruct]:
        """
        This method fetches all records from the WorkflowLinkConstructs table and returns them.
        """
        # Fetch all records from the workflowlinkconstructs table.
        with Session(engine) as session:
            result = session.exec(select(WorkflowLinkConstruct)).all()
            return result
