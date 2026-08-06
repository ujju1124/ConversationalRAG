"""Service for document ingestion: extraction, chunking, embedding, and storage."""
import pdfplumber
import uuid
from typing import List, Tuple
from app.core.embedding_model import generate_embeddings
from app.core.pinecone_client import get_pinecone_index
from app.models.db_models import Document
from sqlalchemy.orm import Session
import nltk

# Download nltk sentence tokenizer data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extract text from PDF or TXT file.
    
    Args:
        file_content: Raw file bytes
        filename: Name of the file (used to determine type)
        
    Returns:
        Extracted text content
        
    Raises:
        ValueError: If file type is not supported
    """
    if filename.endswith('.pdf'):
        # Extract text from PDF using pdfplumber
        import io
        text = ""
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    elif filename.endswith('.txt'):
        # Read text file directly
        return file_content.decode('utf-8')
    else:
        raise ValueError("Unsupported file type. Only .pdf and .txt are allowed.")


def chunk_text_fixed(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into fixed-size chunks with overlap.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Number of overlapping characters between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
        start += (chunk_size - overlap)
    
    return chunks


def chunk_text_sentence(text: str) -> List[str]:
    """
    Split text on sentence boundaries using nltk.
    
    Args:
        text: Text to chunk
        
    Returns:
        List of sentences
    """
    sentences = nltk.sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]


def store_in_pinecone(chunks: List[str], embeddings: List[List[float]], 
                     filename: str, strategy: str, document_id: str) -> None:
    """
    Store embeddings and metadata in Pinecone.
    
    Args:
        chunks: List of text chunks
        embeddings: List of embedding vectors
        filename: Source filename
        strategy: Chunking strategy used
        document_id: Unique document identifier
    """
    pinecone_index = get_pinecone_index()
    vectors = []
    
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector_id = f"{document_id}_{idx}"
        metadata = {
            "chunk_index": idx,
            "source_filename": filename,
            "strategy": strategy,
            "document_id": document_id,
            "text": chunk
        }
        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": metadata
        })
    
    # Upsert vectors in batches of 100 (Pinecone best practice)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        pinecone_index.upsert(vectors=batch)


def save_document_metadata(db: Session, document_id: str, filename: str, 
                          chunk_count: int, strategy: str) -> None:
    """
    Save document metadata to SQLite.
    
    Args:
        db: Database session
        document_id: Unique document identifier
        filename: Source filename
        chunk_count: Number of chunks created
        strategy: Chunking strategy used
    """
    document = Document(
        document_id=document_id,
        filename=filename,
        chunk_count=chunk_count,
        strategy=strategy
    )
    db.add(document)
    db.commit()


def ingest_document(file_content: bytes, filename: str, strategy: str, db: Session) -> Tuple[str, int]:
    """
    Complete document ingestion pipeline.
    
    This function runs synchronously and contains blocking I/O operations.
    FastAPI will automatically run it in a threadpool when called from an async route.
    
    Args:
        file_content: Raw file bytes
        filename: Name of the file
        strategy: Chunking strategy ('fixed' or 'sentence')
        db: Database session
        
    Returns:
        Tuple of (document_id, chunk_count)
        
    Raises:
        ValueError: If strategy is invalid or file type is unsupported
    """
    # Generate unique document ID
    document_id = str(uuid.uuid4())
    
    # Step 1: Extract text
    text = extract_text_from_file(file_content, filename)
    
    # Step 2: Chunk text based on strategy
    if strategy == "fixed":
        chunks = chunk_text_fixed(text)
    elif strategy == "sentence":
        chunks = chunk_text_sentence(text)
    else:
        raise ValueError("Invalid strategy. Must be 'fixed' or 'sentence'.")
    
    # Step 3: Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # Step 4: Store in Pinecone
    store_in_pinecone(chunks, embeddings, filename, strategy, document_id)
    
    # Step 5: Save metadata to SQLite
    save_document_metadata(db, document_id, filename, len(chunks), strategy)
    
    return document_id, len(chunks)
