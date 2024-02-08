"""Main module for the FastAPI application."""
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv, dotenv_values
from backend.app.controllers import workflow_controller  # pylint: disable=import-error
from backend.app.routers import user_router  # pylint: disable=import-error

# load environment variables from .env
load_dotenv(".env")

# access environment variables using os.getenv
AD_SERVER = os.getenv('AD_SERVER')
AD_DOMAIN = os.getenv("AD_DOMAIN")
AD_SEARCH_BASE = os.getenv("AD_SEARCH_BASE")
print("AD_SERVER", AD_SERVER)
print(AD_SERVER, AD_DOMAIN, AD_SEARCH_BASE)

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
app.include_router(workflow_controller.router)
app.include_router(user_router.router, prefix="/users", tags=["users"])

class Workflow(BaseModel):
    """Workflow model."""
    id: int
    name: str
    creator: str

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """Say hello to a user."""
    return {"message": f"Hello {name}"}

@app.get("/workflows/")
def read_workflows(limit: int = 10):
    """Read workflows."""
    return {"workflows": ["workflow1", "workflow2"], "limit": limit}

@app.post("/workflows/", response_model=Workflow)
def create_workflow(workflow: Workflow):
    """Create a workflow."""
    return workflow
