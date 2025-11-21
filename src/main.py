from fastapi import FastAPI
from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command

from src.external_api.router import router as external_router
from src.cat_facts.router import router as cat_facts_router
from src.database.utils import engine
from src.database.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and run migrations
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Run Alembic migrations
    def run_migrations():
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

    run_migrations()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(title="Cat Facts API", lifespan=lifespan)

# Include routers
app.include_router(external_router)
app.include_router(cat_facts_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Cat Facts API with PostgreSQL and Redis!"}
