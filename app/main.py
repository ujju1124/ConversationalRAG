"""Main FastAPI application entry point."""
from fastapi import FastAPI
from app.routers import ingest, chat
from app.core.db import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Conversational RAG Backend",
    description="Production-ready backend with document ingestion and conversational RAG APIs",
    version="1.0.0"
)

# Include routers
app.include_router(ingest.router, tags=["Ingestion"])
app.include_router(chat.router, tags=["Chat"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "Conversational RAG Backend API is running",
        "endpoints": ["/ingest", "/chat"]
    }
