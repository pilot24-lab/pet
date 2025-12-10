from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.infrastructure.database.connection import db_connection
from src.presentation.api.routes.users import router as users_router
from src.presentation.api.routes.comments import router as comments_router
from src.infrastructure.logging_config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger('my_app')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Clean Architecture Template",
        description="FastAPI project template with Clean Architecture principles",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users_router)
    app.include_router(comments_router)

    @app.get("/health")
    async def health_check():
        logger.info("Info message")
        return {"status": "ok"}

    return app


app = create_app()

