from fastapi import FastAPI
from routers import default, weather

app = FastAPI()

# Include the routers
app.include_router(default.router, prefix='/api')
app.include_router(weather.router, prefix='/api')