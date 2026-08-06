"""Centralized embedding model initialization."""
from sentence_transformers import SentenceTransformer
from typing import List, Optional

# Global embedding model instance (loaded once)
_embedding_model: Optional[SentenceTransformer] = None


def get_embedding_model() -> SentenceTransformer:
    """
    Get or initialize the embedding model (lazy singleton pattern).
    
    Returns:
        SentenceTransformer: The embedding model instance
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embedding vectors (384 dimensions each)
    """
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings.tolist()
