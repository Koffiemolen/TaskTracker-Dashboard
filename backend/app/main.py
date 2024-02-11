"""Main module for the FastAPI application."""
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv, dotenv_values
from backend.app.controllers import workflow_controller  # pylint: disable=import-error
from backend.app.routers import user_router, automateapi_router  # pylint: disable=import-error

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
app.include_router(automateapi_router.router, prefix="/automateapi", tags=["automateapi"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    """Say hello to a user."""
    return {"message": f"Hello {name}"}
