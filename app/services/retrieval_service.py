"""Service for retrieving relevant chunks from Pinecone."""
from typing import List
from app.core.embedding_model import generate_embeddings
from app.core.pinecone_client import get_pinecone_index


def retrieve_relevant_chunks(user_message: str, document_id: str, top_k: int = 5) -> List[str]:
    """
    Query Pinecone to retrieve top K most relevant chunks for a user message.
    
    This function contains blocking I/O operations (Pinecone API calls).
    
    Args:
        user_message: User's query text
        document_id: Document ID to filter results
        top_k: Number of chunks to retrieve
        
    Returns:
        List of relevant text chunks
    """
    pinecone_index = get_pinecone_index()
    
    # Step 1: Generate embedding for user message
    query_embedding = generate_embeddings([user_message])[0]
    
    # Step 2: Query Pinecone with document_id filter
    query_response = pinecone_index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={"document_id": {"$eq": document_id}}
    )
    
    # Step 3: Extract text from matches
    chunks = []
    for match in query_response.matches:
        if 'text' in match.metadata:
            chunks.append(match.metadata['text'])
    
    return chunks
