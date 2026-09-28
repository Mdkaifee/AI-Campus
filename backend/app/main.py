"""DAVIET Smart Campus AI Assistant — FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, chat, health
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.database.mongodb import (
    close_mongo_connection,
    connect_to_mongo,
    get_database,
)
from app.repositories.chat_repository import ChatRepository
from app.repositories.error_audit_repository import ErrorAuditRepository
from app.services.ai_service import AIService
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService
from app.services.location_service import LocationService
from app.services.retrieval_service import RetrievalService
from app.services.web_retrieval_service import VERIFIED_DYNAMIC_CATALOG, WebRetrievalService

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info(
        "Starting API | ai_provider=%s | model=%s | cors=%s",
        settings.ai_provider,
        settings.ollama_model,
        settings.cors_origins,
    )
    app.state.db = None
    try:
        await connect_to_mongo()
        app.state.db = get_database()
    except Exception:
        # Keep API up so /api/health can report degraded status clearly
        logger.exception(
            "MongoDB unavailable at startup — API running in degraded mode"
        )

    db = getattr(app.state, "db", None)
    loc_service = LocationService(db)
    web_retriever = WebRetrievalService(db)
    if db is not None:
        try:
            await web_retriever.sync_catalog_to_mongo()
            await loc_service.sync_locations_to_mongo()
        except Exception:
            logger.warning("Could not sync dynamic catalog or locations to MongoDB")

    app.state.auth_service = AuthService(db)
    retrieval = RetrievalService(dynamic_items=VERIFIED_DYNAMIC_CATALOG)
    app.state.chat_service = ChatService(
        retrieval=retrieval,
        ai=AIService(),
        chat_repo=ChatRepository(db),
        audit_repo=ErrorAuditRepository(db),
        location_service=loc_service,
        web_retrieval_service=web_retriever,
    )


    yield

    await close_mongo_connection()
    logger.info("API shutdown complete")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="DAVIET Smart Campus AI Assistant",
        description=(
            "Phase 1 — DAVIET information chatbot API. "
            "Answers are grounded in a college-specific knowledge base (RAG)."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_origin_regex=r"https://.*\.devtunnels\.ms",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "status": "online",
            "message": "DAVIET Smart Campus AI Assistant API is running!",
            "docs": "/docs",
            "health": "/api/health",
        }

    app.include_router(auth.router, prefix="/api")
    app.include_router(health.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception(
            "Unhandled error on %s %s: %s",
            request.method,
            request.url.path,
            type(exc).__name__,
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": (
                    "Something went wrong while processing your request. "
                    "Please try again."
                )
            },
        )

    return app


app = create_app()
