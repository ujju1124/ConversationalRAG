"""Main FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import ingest, chat, sessions
from app.core.db import engine, Base
from app.core.logging_config import get_logger
from app.core.pinecone_client import get_pinecone_index
from app.core.embedding_model import get_embedding_model

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup: Initialize database tables
    logger.info("Starting up application...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Pre-load expensive resources to avoid first-request latency
    try:
        get_embedding_model()
        logger.info("Embedding model loaded successfully")
    except Exception as e:
        logger.warning(f"Failed to pre-load embedding model: {e}")
    
    try:
        get_pinecone_index()
        logger.info("Pinecone index connected successfully")
    except Exception as e:
        logger.warning(f"Failed to connect to Pinecone index: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Conversational RAG Backend",
    description="Production-ready backend with document ingestion and conversational RAG APIs",
    version="1.0.0",
    lifespan=lifespan
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.
    Logs the full traceback server-side and returns a clean JSON error.
    
    Note: HTTPException is handled by FastAPI's built-in handler and won't reach here.
    """
    # Skip HTTPException (FastAPI handles these)
    from fastapi import HTTPException
    if isinstance(exc, HTTPException):
        raise exc
    
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}",
        exc_info=exc
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred"}
    )

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # React default port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router, tags=["Ingestion"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(sessions.router, tags=["Sessions"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "Conversational RAG Backend API is running",
        "endpoints": ["/ingest", "/chat", "/sessions"]
    }
