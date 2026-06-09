# Conversational RAG Backend

A production-ready FastAPI backend system with document ingestion and conversational RAG (Retrieval-Augmented Generation) capabilities. The system supports PDF and TXT file ingestion, semantic search using vector embeddings, and intelligent conversation with booking detection.

## Features

- **Document Ingestion API**: Upload PDF/TXT files and store them as vector embeddings
- **Conversational RAG API**: Chat with documents using context-aware responses
- **Booking Detection**: Automatically detect and extract interview booking information
- **Chat Memory**: Maintain conversation history across sessions using Redis
- **Vector Search**: Semantic search using Pinecone vector database
- **Local Embeddings**: Generate embeddings locally using sentence-transformers

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **Groq API**: LLM text generation (llama3-8b-8192)
- **sentence-transformers**: Local embedding generation (all-MiniLM-L6-v2)
- **Pinecone**: Vector database for semantic search
- **Upstash Redis**: Chat memory and session management
- **SQLite + SQLAlchemy**: Metadata and booking storage
- **pdfplumber**: PDF text extraction
- **NLTK**: Sentence tokenization

## Project Structure

```
app/
├── main.py                      # FastAPI application entry point
├── routers/
│   ├── ingest.py               # Document ingestion endpoint
│   └── chat.py                 # Conversational RAG endpoint
├── services/
│   ├── ingestion_service.py    # Document processing and embedding
│   ├── retrieval_service.py    # Vector search logic
│   ├── memory_service.py       # Redis chat history management
│   ├── llm_service.py          # Groq API integration
│   └── booking_service.py      # Booking detection and extraction
├── models/
│   ├── schemas.py              # Pydantic request/response models
│   └── db_models.py            # SQLAlchemy database models
└── core/
    ├── config.py               # Environment configuration
    ├── db.py                   # Database setup
    ├── pinecone_client.py      # Pinecone initialization
    └── redis_client.py         # Redis initialization
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys and configuration:

```bash
cp .env.example .env
```

Required environment variables:

- `GROQ_API_KEY`: Your Groq API key (get from https://console.groq.com)
- `PINECONE_API_KEY`: Your Pinecone API key (get from https://www.pinecone.io)
- `PINECONE_INDEX_NAME`: Name for your Pinecone index (e.g., "rag-documents")
- `UPSTASH_REDIS_URL`: Your Upstash Redis URL (get from https://upstash.com)
- `UPSTASH_REDIS_TOKEN`: Your Upstash Redis token
- `DATABASE_URL`: SQLite database path (default: `sqlite:///./app.db`)

### 3. Run the Server

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

### 1. Document Ingestion API

**Endpoint**: `POST /ingest`

Upload a PDF or TXT file and generate embeddings.

**Parameters**:
- `file` (form-data): PDF or TXT file to upload
- `strategy` (query param): Chunking strategy - either `fixed` or `sentence`
  - `fixed`: 500 character chunks with 50 character overlap
  - `sentence`: Sentence-based chunking using NLTK

**Example Request**:

```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Example Response**:

```json
{
  "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "document.pdf",
  "chunk_count": 42,
  "strategy": "sentence"
}
```

### 2. Conversational RAG API

**Endpoint**: `POST /chat`

Chat with a document using retrieval-augmented generation.

**Request Body**:

```json
{
  "session_id": "user123-session",
  "user_message": "What are the main topics discussed?",
  "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Example Request**:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123-session",
    "user_message": "What are the main topics discussed?",
    "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }'
```

**Example Response (without booking)**:

```json
{
  "response": "Based on the context, the main topics discussed are...",
  "session_id": "user123-session",
  "booking": null
}
```

**Example Response (with booking)**:

```json
{
  "response": "I'd be happy to schedule an interview for you...",
  "session_id": "user123-session",
  "booking": {
    "name": "John Doe",
    "email": "john@example.com",
    "date": "2024-03-15",
    "time": "2:00 PM"
  }
}
```

## Booking Detection

The system automatically detects booking intent when users use keywords like:
- book
- schedule
- interview
- appointment
- available
- meeting
- slot

When detected, it extracts structured information (name, email, date, time) and stores it in the database.

## Architecture Highlights

### Document Ingestion Flow
1. Extract text from PDF/TXT file
2. Chunk text using fixed-size or sentence-based strategy
3. Generate 384-dimensional embeddings using all-MiniLM-L6-v2
4. Store embeddings in Pinecone with metadata
5. Save document metadata to SQLite

### Conversational RAG Flow
1. Convert user message to embedding
2. Query Pinecone for top 5 relevant chunks (filtered by document_id)
3. Fetch last 6 messages from Redis chat history
4. Build prompt with system instructions, context, history, and user message
5. Generate response using Groq API (llama3-8b-8192)
6. Save conversation turn to Redis
7. Detect booking intent and extract information if present
8. Return response with optional booking data

## Database Schema

### Documents Table
- `document_id` (Primary Key)
- `filename`
- `upload_time`
- `chunk_count`
- `strategy`

### Bookings Table
- `booking_id` (Primary Key)
- `session_id`
- `name`
- `email`
- `date`
- `time`
- `created_at`

## Development Notes

- All functions include type annotations and docstrings
- Pydantic models enforce request/response validation
- Environment variables loaded via pydantic-settings
- Async endpoints where applicable
- Comprehensive error handling with HTTP status codes
- No LangChain RetrievalQAChain - manual retrieval implementation
- Local embeddings (no external API calls for embeddings)

## License

MIT
