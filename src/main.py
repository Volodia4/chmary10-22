from fastapi import FastAPI
from scr.database.utils import create_tables
from scr.external_api import router as external_router
from scr.cat_facts.router import router as cat_facts_router

# Create database tables
create_tables()

app = FastAPI(
    title="FastAPI Cat Facts & External APIs",
    description="Comprehensive API with external integrations and database operations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(external_router.router)
app.include_router(cat_facts_router.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to FastAPI Cat Facts API",
        "endpoints": {
            "external_api": "/docs#/External%20API",
            "cat_facts": "/docs#/Cat%20Facts%20Database"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Cat Facts API",
        "version": "2.0.0"
    }

@app.get("/info")
def api_info():
    return {
        "name": "FastAPI Cat Facts API",
        "version": "2.0.0",
        "description": "Integration with external APIs and database operations",
        "modules": [
            "external_api - External API integrations",
            "cat_facts - Database operations with Cat Facts"
        ]
    }
