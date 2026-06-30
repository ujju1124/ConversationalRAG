# Conversational RAG Backend

A production-ready FastAPI backend system with document ingestion and conversational RAG (Retrieval-Augmented Generation) capabilities. The system supports PDF and TXT file ingestion, semantic search using vector embeddings, intelligent conversation with chat memory, and automatic booking intent detection.

> **Note**: This is a backend-only project. A Postman collection and curl examples are provided for easy API verification without requiring a frontend.

## Features

- **Document Ingestion API**: Upload PDF/TXT files with configurable chunking strategies (sentence-based or fixed-size)
- **Conversational RAG**: Chat with documents using context-aware responses powered by Groq LLM
- **Booking Intent Detection**: Automatically detect and extract structured booking information (name, email, date, time)
- **Chat Memory**: Persistent conversation history using Redis (fast context) and SQLite (persistent storage)
- **Vector Search**: Semantic search using Pinecone vector database with local embeddings
- **Session History**: Track all conversations with full message history and session metadata
- **Local Embeddings**: Generate 384-dimensional embeddings using sentence-transformers (all-MiniLM-L6-v2)


## Tech Stack

- **FastAPI**: Modern web framework for building APIs with automatic OpenAPI documentation
- **Groq API**: Ultra-fast LLM inference (llama3-8b-8192)
- **sentence-transformers**: Local embedding generation (all-MiniLM-L6-v2, 384 dimensions)
- **Pinecone**: Serverless vector database for semantic search
- **Upstash Redis**: Serverless Redis for fast chat context retrieval
- **SQLite + SQLAlchemy**: Persistent storage for messages, sessions, and bookings
- **pdfplumber**: Reliable PDF text extraction
- **NLTK**: Sentence tokenization for intelligent chunking
- **Pydantic**: Type validation for API requests and LLM outputs

## Project Structure

```
app/
├── main.py                      # FastAPI application entry point
├── routers/
│   ├── ingest.py               # Document ingestion endpoint
│   ├── chat.py                 # Conversational RAG endpoint
│   └── sessions.py             # Session history management
├── services/
│   ├── ingestion_service.py    # Document processing and embedding
│   ├── retrieval_service.py    # Vector search logic
│   ├── memory_service.py       # Redis + SQLite persistence
│   ├── llm_service.py          # Groq API integration
│   └── booking_service.py      # Booking detection and extraction
├── models/
│   ├── schemas.py              # Pydantic request/response models
│   └── db_models.py            # SQLAlchemy ORM models
└── core/
    ├── config.py               # Environment configuration
    ├── db.py                   # Database setup
    ├── pinecone_client.py      # Pinecone initialization
    └── redis_client.py         # Redis initialization
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- API keys for: Groq, Pinecone, Upstash Redis (all have free tiers)

### 1. Clone and Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required environment variables:

- `GROQ_API_KEY`: Get from https://console.groq.com (free tier: 14,400 requests/day)
- `PINECONE_API_KEY`: Get from https://www.pinecone.io (free tier: 1 index, 100K vectors)
- `PINECONE_INDEX_NAME`: Name for your Pinecone index (e.g., "rag-documents")
- `UPSTASH_REDIS_URL`: Get from https://upstash.com (free tier: 10K commands/day)
- `UPSTASH_REDIS_TOKEN`: Your Upstash Redis token
- `DATABASE_URL`: SQLite database path (default: `sqlite:///./app.db`)

### 3. Run the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (interactive Swagger UI)

### 4. Verify Installation

```bash
curl http://localhost:8000/
```

You should see:
```json
{
  "status": "online",
  "message": "Conversational RAG Backend API is running",
  "endpoints": ["/ingest", "/chat", "/sessions"]
}
```

## Try It Yourself

The backend can be tested without a frontend using either **Postman** or **curl commands**. All examples below use real API responses captured from actual requests.

### Option 1: Using Postman (Recommended)

A complete Postman collection is included in the repository with all endpoints pre-configured and real response examples.

**Steps:**

1. **Import the collection**:
   - Open Postman
   - Click "Import" → "File"
   - Select `ConversationalRAG.postman_collection.json` from this repository
   
2. **Update the document path** (Request #2 "Ingest Document"):
   - In the "Body" tab, update the file path to point to `sample_document.txt` in your local repo
   
3. **Run the requests in order**:
   - Start with "1. Health Check" to verify the server is running
   - Run "2. Ingest Document" - this automatically saves the `document_id` for subsequent requests
   - Run the chat requests (4-6) - they use the saved `document_id` automatically
   - Test session management with requests 7-9

**Collection Variables:**
- `base_url`: `http://localhost:8000` (default)
- `session_id`: `postman-test-session` (you can change this)
- `document_id`: Auto-populated after ingestion

---

### Option 2: Using curl Commands

If you don't have Postman, use these curl commands. Make sure the backend server is running first.

#### 1. Health Check

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "online",
  "message": "Conversational RAG Backend API is running",
  "endpoints": ["/ingest", "/chat", "/sessions"]
}
```

---

#### 2. Ingest Document

Upload `sample_document.txt` (included in repo) with sentence-based chunking:

**Windows (PowerShell):**
```powershell
curl.exe -X POST "http://localhost:8000/ingest?strategy=sentence" `
  -F "file=@sample_document.txt"
```

**Linux/Mac:**
```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -F "file=@sample_document.txt"
```

**Response:**
```json
{
  "document_id": "7d4b9197-d256-481d-b5b2-a1ec2653d73d",
  "filename": "sample_document.txt",
  "chunk_count": 21,
  "strategy": "sentence"
}
```

> **Note**: Save the `document_id` - you'll need it for chat requests.

---

#### 3. Chat - Ask a Question

Replace `YOUR_DOCUMENT_ID` with the `document_id` from step 2:

**Windows (PowerShell):**
```powershell
curl.exe -X POST "http://localhost:8000/chat" `
  -H "Content-Type: application/json" `
  -d '{\"session_id\":\"test-session\",\"user_message\":\"What is machine learning?\",\"document_id\":\"YOUR_DOCUMENT_ID\"}'
```

**Linux/Mac:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "user_message": "What is machine learning?",
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

**Response:**
```json
{
  "response": "Machine learning is a subset of AI that enables systems to learn and improve from experience.",
  "session_id": "test-session",
  "booking": null
}
```

---

#### 4. Chat - Test Booking Detection

**Windows (PowerShell):**
```powershell
curl.exe -X POST "http://localhost:8000/chat" `
  -H "Content-Type: application/json" `
  -d '{\"session_id\":\"test-session\",\"user_message\":\"I want to schedule an interview for Alice Johnson at alice.johnson@email.com on December 25th at 2:30 PM\",\"document_id\":\"YOUR_DOCUMENT_ID\"}'
```

**Linux/Mac:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "user_message": "I want to schedule an interview for Alice Johnson at alice.johnson@email.com on December 25th at 2:30 PM",
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

**Response:**
```json
{
  "response": "However, I notice that the preferred date you provided, December 25th, falls on a holiday...",
  "session_id": "test-session",
  "booking": {
    "name": "Alice Johnson",
    "email": "alice.johnson@email.com",
    "date": "December 25th",
    "time": "2:30 PM"
  }
}
```

---

#### 5. Chat - Test Context Memory

Ask a follow-up question using the same `session_id`:

**Windows (PowerShell):**
```powershell
curl.exe -X POST "http://localhost:8000/chat" `
  -H "Content-Type: application/json" `
  -d '{\"session_id\":\"test-session\",\"user_message\":\"What types of machine learning did you mention?\",\"document_id\":\"YOUR_DOCUMENT_ID\"}'
```

**Linux/Mac:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "user_message": "What types of machine learning did you mention?",
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

**Response:**
```json
{
  "response": "I mentioned three main types: supervised learning, unsupervised learning, and reinforcement learning.",
  "session_id": "test-session",
  "booking": null
}
```

> **Notice**: The system remembered the previous conversation!

---

#### 6. Get All Sessions

```bash
curl http://localhost:8000/sessions
```

**Response:**
```json
[
  {
    "session_id": "test-session",
    "document_id": "7d4b9197-d256-481d-b5b2-a1ec2653d73d",
    "document_name": "sample_document.txt",
    "title": "What is machine learning?",
    "created_at": "2026-06-30T08:39:22.250357",
    "updated_at": "2026-06-30T08:39:29.996189",
    "message_count": 6
  }
]
```

---

#### 7. Get Session Messages

Replace `test-session` with your actual session ID:

```bash
curl http://localhost:8000/sessions/test-session/messages
```

**Response:**
```json
[
  {
    "id": 1,
    "role": "user",
    "content": "What is machine learning?",
    "has_booking": false,
    "created_at": "2026-06-30T08:39:23.698901"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "Machine learning is a subset of AI...",
    "has_booking": false,
    "created_at": "2026-06-30T08:39:23.705002"
  }
]
```

---

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## API Endpoints

### 1. Health Check
- **GET** `/`
- **Description**: Verify server is running
- **Response**: Server status and available endpoints

### 2. Document Ingestion
- **POST** `/ingest?strategy={sentence|fixed}`
- **Parameters**: 
  - `file` (form-data): PDF or TXT file
  - `strategy` (query): Chunking strategy
    - `sentence`: Sentence-based chunking using NLTK
    - `fixed`: 500 chars with 50 char overlap
- **Response**: `document_id`, `filename`, `chunk_count`, `strategy`

### 3. Conversational Chat
- **POST** `/chat`
- **Body**: 
  ```json
  {
    "session_id": "string",
    "user_message": "string",
    "document_id": "string"
  }
  ```
- **Response**: `response`, `session_id`, `booking` (if detected)

### 4. Get All Sessions
- **GET** `/sessions`
- **Description**: List all chat sessions ordered by recent activity
- **Response**: Array of session summaries with metadata

### 5. Get Session Messages
- **GET** `/sessions/{session_id}/messages`
- **Description**: Retrieve complete message history for a session
- **Response**: Array of messages in chronological order

### 6. Delete Session
- **DELETE** `/sessions/{session_id}`
- **Description**: Remove session and all messages from DB and Redis
- **Response**: Deletion confirmation



## Architecture Highlights

### Document Ingestion Flow
1. Extract text from PDF/TXT file using pdfplumber
2. Chunk text using selected strategy:
   - **Sentence**: NLTK sentence tokenization (preserves semantic boundaries)
   - **Fixed**: 500 chars with 50 char overlap (ensures context continuity)
3. Generate 384-dimensional embeddings using all-MiniLM-L6-v2 (local, fast)
4. Store embeddings in Pinecone with metadata (document_id, chunk_index, text)
5. Save document metadata to SQLite (filename, chunk_count, strategy, timestamp)

### Conversational RAG Flow
1. Convert user message to 384-d embedding vector
2. Query Pinecone for top 5 relevant chunks (filtered by document_id, cosine similarity)
3. Fetch last 6 messages from Redis for conversation context
4. Build structured prompt:
   - System instructions (RAG behavior, booking detection rules)
   - Retrieved context chunks
   - Chat history
   - Current user message
5. Generate response using Groq API (llama3-8b-8192, ~400 tokens/sec)
6. Save conversation turn to:
   - **Redis**: Fast context retrieval for next turn (TTL: 1 hour)
   - **SQLite**: Persistent message history with session metadata
7. Detect booking intent using keyword matching + LLM extraction
8. Return response with optional structured booking data

### Booking Detection Pipeline
1. **Keyword detection**: Check for booking-related terms (schedule, interview, book, appointment, etc.)
2. **LLM extraction**: If detected, use structured JSON mode with Pydantic validation
3. **Data validation**: Extract name, email, date, time with format checking
4. **Database storage**: Save to bookings table with session reference
5. **Response**: Return both conversational response and structured booking object

## Database Schema

### Documents Table
- `document_id` (String, Primary Key, UUID)
- `filename` (String)
- `upload_time` (DateTime)
- `chunk_count` (Integer)
- `strategy` (String: "sentence" or "fixed")

### ChatSessions Table
- `session_id` (String, Primary Key, UUID)
- `document_id` (String, Foreign Key → documents.document_id)
- `document_name` (String)
- `title` (String, nullable) - First user message truncated to 50 chars
- `created_at` (DateTime)
- `updated_at` (DateTime) - Updated on every new message

### ChatMessages Table
- `id` (Integer, Primary Key, Auto-increment)
- `session_id` (String, Foreign Key → chat_sessions.session_id)
- `role` (String: "user" or "assistant")
- `content` (Text)
- `has_booking` (Boolean)
- `created_at` (DateTime)

### Bookings Table
- `booking_id` (Integer, Primary Key, Auto-increment)
- `session_id` (String, Foreign Key → chat_sessions.session_id)
- `name` (String)
- `email` (String)
- `date` (String)
- `time` (String)
- `created_at` (DateTime)

---

## Known Limitations

This project was built as a learning exercise and proof-of-concept. While functional, it has several limitations:

### Testing & Quality Assurance
- **No automated tests**: No unit tests, integration tests, or end-to-end tests implemented
- **No CI/CD pipeline**: Manual deployment and testing only
- **Limited error handling**: Basic try-catch blocks, not comprehensive
- **No load testing**: Performance under concurrent requests not measured

### Booking Detection
- **Accuracy not measured**: No precision/recall metrics or evaluation dataset
- **Keyword-based trigger**: May miss bookings without specific keywords
- **Date parsing limitations**: Relies on LLM interpretation, no formal date parser
- **No timezone handling**: All times treated as local, no UTC conversion
- **No calendar integration**: Booking data stored but not connected to actual calendars

### RAG System
- **No reranking**: Uses Pinecone similarity scores directly, no cross-encoder reranking
- **Fixed chunk size**: No dynamic chunking based on semantic boundaries
- **No multi-document chat**: Each session tied to single document
- **No source attribution**: Doesn't return which chunks were used in response
- **No streaming**: Responses returned in one batch, not streamed token-by-token

### Production Readiness
- **No authentication**: All endpoints publicly accessible
- **No rate limiting**: Vulnerable to abuse
- **No monitoring**: No logging, metrics, or alerting
- **SQLite in production**: Not recommended for concurrent writes
- **Secrets in .env**: No secrets management system
- **No Docker setup**: Manual Python environment required
- **No CORS configuration**: Not configured for cross-origin requests

### Scalability
- **Single-threaded**: No async workers or queue system
- **No caching layer**: Embeddings regenerated on each upload
- **Redis TTL fixed**: No configurable session expiry
- **No batch processing**: Documents processed one at a time

### Documentation
- **No API versioning**: Breaking changes could affect clients
- **Limited inline comments**: Not all functions have docstrings
- **No architecture diagrams**: Text-only architecture description

---

Despite these limitations, the system successfully demonstrates:
✅ RAG implementation from scratch without LangChain  
✅ Vector search with Pinecone  
✅ Conversational memory with Redis + SQLite  
✅ Structured LLM outputs with Pydantic  
✅ RESTful API design with FastAPI  
✅ Dual chunking strategies  

Future improvements would focus on testing, production hardening, and scalability enhancements.





## License

MIT

---

## Contact

Built by **Ujwal**  
GitHub: [ujju1124](https://github.com/ujju1124)

**Project Repository**: [ConversationalRAG](https://github.com/ujju1124/ConversationalRAG)
