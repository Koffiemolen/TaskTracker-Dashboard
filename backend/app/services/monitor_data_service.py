"""Service class to monitor data changes in the Automate database."""
import asyncio
from datetime import datetime, timedelta
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
from backend.app.models import monitor_automate_serversettings  # pylint: disable=import-error

class MonitorDataService:
    """Service class to monitor data changes in the Automate database."""
    def __init__(self, source_db_url: str, poll_interval_seconds=30):
        self.source_engine = create_engine(source_db_url)
        self.source_session_local = sessionmaker(autocommit=False, autoflush=False,
                                                 bind=self.source_engine)
        self.last_check = datetime.utcnow() - timedelta(seconds=5)
        self.poll_interval = poll_interval_seconds  # Define polling interval

    async def transfer_data_triggers(self):
        """Transfers data for the triggers."""
        transfer_sql = text("""
    SELECT [TriggerID], [TriggerName], [TriggerType], [Source], [ScheduleType], [LastLaunchDate], [NextLaunchDate], [Frequency]
    FROM [Automate11].[dbo].[ConsolidatedTriggerInfo]
    """)
        await run_in_threadpool(self._sync_transfer_data, transfer_sql)

    def _sync_transfer_data(self, sql_statement):
        """Synchronizes the transfer of data."""
        with self.source_session_local() as session:  # Corrected to use the source session
            session.execute(sql_statement)
            session.commit()

    async def poll_for_changes_async(self):
        """Asynchronously polls for changes."""
        while True:
            await run_in_threadpool(self._sync_poll_for_changes)
            await asyncio.sleep(self.poll_interval)

    def _sync_poll_for_changes(self):
        """Synchronous method that polls for changes in the database."""
        with self.source_session_local() as session:
            query = select(monitor_automate_serversettings).where(
                monitor_automate_serversettings.last_updated > self.last_check)
            results = session.execute(query).scalars().all()
            for row in results:
                print(f"Found changed row: {row}")
            self.last_check = datetime.utcnow()
