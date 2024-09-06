from fastapi import FastAPI
from routers import register_routers
from base import settings, logger

# Initialize the logger and log the startup messages
logger.info("Starting the FastAPI application")
logger.info(f'Running on {settings.host}:{settings.port}, Debug mode: {settings.debug}')

# Print extra fields only if they exist
extra_fields_message = settings.print_extra_fields()
if extra_fields_message:
    logger.info(extra_fields_message)

app = FastAPI()

register_routers(app)