"""Main module for the FastAPI application."""
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from dotenv import load_dotenv, dotenv_values
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
# load environment variables from .env
load_dotenv(".env")

# import routers and services
from backend.app.routers import user_router, automateapi_router, database_router  # pylint: disable=import-error, wrong-import-position
from backend.app.services.data_aggregation_service import DataAggregationService  # pylint: disable=import-error, wrong-import-position
from backend.app.controllers import workflow_controller  # pylint: disable=import-error, wrong-import-position


# access environment variables using os.getenv
AD_SERVER = os.getenv('AD_SERVER')
AD_DOMAIN = os.getenv("AD_DOMAIN")
AD_SEARCH_BASE = os.getenv("AD_SEARCH_BASE")

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
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(automateapi_router.router, prefix="/automateapi", tags=["automateapi"])
app.include_router(database_router.router, prefix="/automatedb", tags=["automatedb"])

security = HTTPBearer()

@app.on_event("startup")
async def start_scheduler():
    """Start the scheduler."""
    # Create an instance of DataAggregationService
    data_aggregation_service = DataAggregationService(
        source_db_url=os.getenv('AUTOMATE_DB_CONNECTION_STRING'),
        target_db_url=os.getenv('TASKTRACKER_DB_CONNECTION_STRING')
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        data_aggregation_service.transfer_data,  # Use the instance method
        trigger=IntervalTrigger(seconds=20)  # For example, every hour
    )
    scheduler.start()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """Say hello to a user."""
    return {"message": f"Hello {name}"}
