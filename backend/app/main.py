"""Main module for the FastAPI application."""
# main.py
import os
import asyncio
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from fastapi.security import HTTPBearer
from dotenv import load_dotenv, dotenv_values
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from starlette.websockets import WebSocketDisconnect
from backend.app.websocket_manager import manager  # pylint: disable=import-error

# load environment variables from .env
load_dotenv(".env")

# import routers and services
from backend.app.services.monitor_data_service import \
    MonitorDataService  # pylint: disable=import-error, wrong-import-position
from backend.app.routers import user_router, automateapi_router, \
    database_router  # pylint: disable=import-error, wrong-import-position
from backend.app.services.data_aggregation_service import \
    DataAggregationService  # pylint: disable=import-error, wrong-import-position
from backend.app.controllers import workflow_controller  # pylint: disable=import-error, wrong-import-position
from backend.app.controllers import task_controller  # pylint: disable=import-error, wrong-import-position

# access environment variables using os.getenv
AD_SERVER = os.getenv('AD_SERVER')
AD_DOMAIN = os.getenv("AD_DOMAIN")
AD_SEARCH_BASE = os.getenv("AD_SEARCH_BASE")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL_AUTOMATE")

config = dotenv_values(".env")
print("config ", config)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(workflow_controller.router, prefix="/workflows", tags=["workflows"])
app.include_router(task_controller.router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(automateapi_router.router, prefix="/automateapi", tags=["automateapi"])
app.include_router(database_router.router, prefix="/automatedb", tags=["automatedb"])

security = HTTPBearer()

monitor = MonitorDataService(os.getenv('AUTOMATE_DB_CONNECTION_STRING'))

task_scheduler = AsyncIOScheduler()
data_scheduler = AsyncIOScheduler()
last_check_time = datetime.utcnow()

@app.on_event("startup")
async def start_scheduler():
    """Start the scheduler and add tasks with staggered start times."""
    # Create an instance of DataAggregationService
    data_aggregation_service = DataAggregationService(
        source_db_url=os.getenv('AUTOMATE_DB_CONNECTION_STRING'),
        target_db_url=os.getenv('TASKTRACKER_DB_CONNECTION_STRING')
    )

    # Retrieve server settings data
    task_scheduler.add_job(
        data_aggregation_service.transfer_automate_server_settings,
        trigger=IntervalTrigger(seconds=3)
    )

    # Wrap the async function for scheduling
    task_scheduler.add_job(
        data_aggregation_service.monitor_table_changes,
        'interval',
        seconds=5,
    )

    # Retrieve workflow data
    task_scheduler.add_job(
        data_aggregation_service.transfer_data_workflow,
        trigger=IntervalTrigger(seconds=7)
    )

    # Retrieve schedule data
    task_scheduler.add_job(
        data_aggregation_service.transfer_data_triggers,
        trigger=IntervalTrigger(seconds=33)
    )

    # Retrieve agent data
    task_scheduler.add_job(
        data_aggregation_service.transfer_data_agents,
        trigger=IntervalTrigger(seconds=21)
    )

    # Retrieve task data
    task_scheduler.add_job(
        data_aggregation_service.transfer_data_tasks,
        trigger=IntervalTrigger(seconds=6)
    )

    # Retrieve task data
    task_scheduler.add_job(
        data_aggregation_service.transfer_data_tasks,
        trigger=IntervalTrigger(seconds=6)
    )

    # Add the new job for checking workflow updates
    task_scheduler.add_job(
        data_aggregation_service.check_for_workflow_update,
        'interval',
        seconds=10,  # Adjust the interval as per requirement
        next_run_time=datetime.utcnow()  # Start checking for updates immediately upon startup
    )

    task_scheduler.add_job(
        data_aggregation_service.check_for_task_update,
        'interval',
        seconds=10,  # Adjust the interval as per requirement
        next_run_time=datetime.utcnow()  # Start checking for updates immediately upon startup
    )

    # Data sync scheduler
    task_scheduler.start()



@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown the scheduler."""
    monitor.source_engine.dispose()
    task_scheduler.shutdown()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """Say hello to a user."""
    return {"message": f"Hello {name}"}

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    """
    An asynchronous websocket endpoint that defines the behavior of websocket
    connections on a per channel basis.

    Once a connection is established, a message is sent to the client to acknowledge this.
    An infinite loop
    is then entered where the behavior can be handled as per your application's
    needs (asynchronously).

    If the client disconnects at any point, it is safely removed from the manager and
    the connection is severed.

    Parameters:
        websocket (WebSocket): The WebSocket connection object.
        channel (str): The name of the channel the WebSocket is connected to.

    Raises:
        WebSocketDisconnect: If the WebSocket connection is dropped or disconnected.

    """
    try:
        await manager.connect(websocket, channel)
        # await websocket.send_text("WebSocket connection established")
        await websocket.send_text(json.dumps({"message": "WebSocket connection established"}))
        while True:
            # Depending on your application's logic, might wait for a message
            # from the client
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
