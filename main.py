from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import connect_to_mongo, close_mongo_connection
from routes import job_routes, auth_routes
from core.config import settings
from contextlib import asynccontextmanager

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add event handlers for database connection
#app.add_event_handler("startup", connect_to_mongo)
#app.add_event_handler("shutdown", close_mongo_connection)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Include API routers
app.include_router(auth_routes.router, tags=["Authentication"], prefix="/auth")
app.include_router(job_routes.router, tags=["Jobs"], prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    """A simple root endpoint to check if the server is running."""
    return {"message": "Welcome to the College Referral API!"}
