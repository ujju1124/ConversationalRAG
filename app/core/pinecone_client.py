"""Pinecone vector database client initialization."""
from pinecone import Pinecone, ServerlessSpec, Index
from app.core.config import settings

# Global Pinecone client and index (lazy-loaded)
_pc: Pinecone | None = None
_pinecone_index: Index | None = None


def get_pinecone_client() -> Pinecone:
    """
    Get or initialize the Pinecone client (lazy singleton pattern).
    
    Returns:
        Pinecone: The Pinecone client instance
    """
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return _pc


def get_pinecone_index() -> Index:
    """
    Get or create Pinecone index (lazy singleton pattern).
    
    This function is called on first use, not at import time.
    
    Returns:
        Index: The Pinecone index instance
    """
    global _pinecone_index
    
    if _pinecone_index is None:
        pc = get_pinecone_client()
        index_name = settings.PINECONE_INDEX_NAME
        
        # Check if index exists, if not create it
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=384,  # all-MiniLM-L6-v2 produces 384-dimensional embeddings
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
        
        _pinecone_index = pc.Index(index_name)
    
    return _pinecone_index
