# /routers/router_registration.py
from fastapi import FastAPI
from routers import default, weather
from base import logger

def register_routers(app: FastAPI):
    """Register API routers with dynamic prefixes."""
    api_versions = ["/api", "/api/v1"]

    # Include the routers with version prefixes dynamically
    for prefix in api_versions:
        app.include_router(default.router, prefix=prefix)
        app.include_router(weather.router, prefix=prefix)

    # Print all available endpoints
    print_available_endpoints(app)

def print_available_endpoints(app: FastAPI):
    """Prints all available endpoints in the FastAPI application."""
    for route in app.routes:
        if hasattr(route, 'methods'):
            methods = ", ".join(route.methods)
            logger.info(f"Endpoint: {route.path}, Methods: {methods}, Name: {route.name}")
