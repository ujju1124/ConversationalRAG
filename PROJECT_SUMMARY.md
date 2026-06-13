# 📋 Project Summary: Conversational RAG Backend

## ✅ What Was Built

A production-ready FastAPI backend system with two main APIs:

### 1. **Document Ingestion API** (`POST /ingest`)
- Accepts PDF or TXT file uploads
- Supports two chunking strategies:
  - **Fixed**: 500 character chunks with 50 character overlap
  - **Sentence**: Sentence-boundary based chunking using NLTK
- Generates 384-dimensional embeddings using `all-MiniLM-L6-v2`
- Stores vectors in Pinecone with rich metadata
- Saves document metadata to SQLite

### 2. **Conversational RAG API** (`POST /chat`)
- Retrieves top 5 relevant chunks from Pinecone
- Maintains chat history (last 6 messages) in Redis
- Generates contextual responses using Groq (llama3-8b-8192)
- **Automatically detects booking intent** with keywords
- Extracts structured booking information (name, email, date, time)
- Stores bookings in SQLite database

---

## 🏗️ Architecture

### Tech Stack
- **Framework**: FastAPI (async, modern, fast)
- **Embeddings**: sentence-transformers (local, no API calls)
- **LLM**: Groq API with llama3-8b-8192
- **Vector DB**: Pinecone (free tier, serverless)
- **Cache/Memory**: Upstash Redis (free tier)
- **Database**: SQLite with SQLAlchemy
- **PDF Processing**: pdfplumber
- **Text Processing**: NLTK

### Services Architecture
```
┌─────────────────────────────────────────────┐
│          FastAPI Application                │
├─────────────────────────────────────────────┤
│  Routers                                    │
│  ├── /ingest    (Document Upload)          │
│  └── /chat      (Conversational RAG)       │
├─────────────────────────────────────────────┤
│  Services                                   │
│  ├── Ingestion  (Extract, Chunk, Embed)    │
│  ├── Retrieval  (Vector Search)            │
│  ├── Memory     (Chat History)             │
│  ├── LLM        (Response Generation)      │
│  └── Booking    (Intent Detection)         │
├─────────────────────────────────────────────┤
│  Core Infrastructure                        │
│  ├── Pinecone  (Vector Storage)            │
│  ├── Redis     (Session Memory)            │
│  ├── SQLite    (Metadata & Bookings)       │
│  └── Config    (Environment Variables)     │
└─────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Conversational_RAG/
├── app/
│   ├── main.py                         # FastAPI entry point
│   ├── routers/
│   │   ├── ingest.py                   # Document ingestion endpoint
│   │   └── chat.py                     # Chat endpoint
│   ├── services/
│   │   ├── ingestion_service.py        # Text extraction, chunking, embedding
│   │   ├── retrieval_service.py        # Pinecone query
│   │   ├── memory_service.py           # Redis chat history
│   │   ├── llm_service.py              # Groq API calls
│   │   └── booking_service.py          # Booking detection & extraction
│   ├── models/
│   │   ├── schemas.py                  # Pydantic models
│   │   └── db_models.py                # SQLAlchemy tables
│   └── core/
│       ├── config.py                   # Environment configuration
│       ├── db.py                       # Database setup
│       ├── pinecone_client.py          # Vector DB client
│       └── redis_client.py             # Redis client
├── .env                                # API keys (NOT in git)
├── .env.example                        # Template for environment variables
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
├── run_server.py                       # Simple server runner
├── sample_document.txt                 # Test document
├── README.md                           # Full documentation
├── GETTING_STARTED.md                  # Quick start guide
└── PROJECT_SUMMARY.md                  # This file
```

---

## 🔑 Environment Configuration

All sensitive credentials are stored in `.env`:

```env
GROQ_API_KEY=gsk_...                           # Groq LLM API
PINECONE_API_KEY=pcsk_...                      # Pinecone vector DB
PINECONE_INDEX_NAME=conversational-rag         # Your index name
UPSTASH_REDIS_URL=rediss://...upstash.io       # Redis URL
UPSTASH_REDIS_TOKEN=...                        # Redis auth token
DATABASE_URL=sqlite:///./app.db                # SQLite path
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
- Copy `.env.example` to `.env`
- Fill in your API keys

### 3. Start Server
```bash
python run_server.py
# OR
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access APIs
- Health Check: `http://localhost:8000/`
- Interactive Docs: `http://localhost:8000/docs`
- Ingest Endpoint: `http://localhost:8000/ingest`
- Chat Endpoint: `http://localhost:8000/chat`

---

## 🧪 Testing Flow

### Step 1: Upload a Document
```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -F "file=@sample_document.txt"
```

Response: `{"document_id": "xxx", "chunk_count": 12, ...}`

### Step 2: Chat with the Document
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "user_message": "What is machine learning?",
    "document_id": "xxx"
  }'
```

### Step 3: Test Booking Detection
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "user_message": "I want to book an interview for Alice at alice@email.com on Friday at 3 PM",
    "document_id": "xxx"
  }'
```

Response includes extracted booking information.

---

## 📊 Database Tables

### Documents Table
| Field | Type | Description |
|-------|------|-------------|
| document_id | String (PK) | Unique document identifier |
| filename | String | Original filename |
| upload_time | DateTime | When uploaded |
| chunk_count | Integer | Number of chunks created |
| strategy | String | Chunking strategy used |

### Bookings Table
| Field | Type | Description |
|-------|------|-------------|
| booking_id | String (PK) | Unique booking ID |
| session_id | String | Chat session ID |
| name | String | Extracted name |
| email | String | Extracted email |
| date | String | Extracted date |
| time | String | Extracted time |
| created_at | DateTime | When booking was created |

---

## 🎯 Key Features

✅ **No Hardcoded Keys** - All credentials from environment  
✅ **Type Annotations** - Full type hints on all functions  
✅ **Docstrings** - One-line docstring per function  
✅ **Error Handling** - Try/except in all endpoints  
✅ **Pydantic Validation** - Request/response validation  
✅ **Separation of Concerns** - Clean service layer architecture  
✅ **Manual RAG** - No LangChain RetrievalQAChain  
✅ **Local Embeddings** - No external embedding API  
✅ **Async Endpoints** - FastAPI async where possible  
✅ **Clean Git History** - Logical, incremental commits  

---

## 📈 Free Tier Limits

### Groq
- 30 requests/minute
- 6,000 requests/day

### Pinecone
- 1 pod (serverless)
- 100K vectors
- 1GB storage

### Upstash Redis
- 10,000 commands/day

---

## 🔗 GitHub Repository

**Repository**: https://github.com/ujju1124/ConversationalRAG

### Commit History
1. init: project structure and gitignore
2. core: config, database, pinecone and redis clients
3. models: database models and pydantic schemas
4. service: document ingestion — extraction, chunking, embeddings
5. service: retrieval — pinecone query logic
6. service: memory — redis chat history
7. service: llm — groq api integration
8. service: booking — intent detection and storage
9. router: ingest and chat endpoints
10. app: fastapi entry point
11. docs: requirements and readme
12. init: app and services module markers

---

## 🎓 What You Learned

- Building production FastAPI applications
- Vector embeddings and semantic search
- RAG (Retrieval-Augmented Generation) patterns
- Pinecone vector database integration
- Redis for session management
- Groq API for fast LLM inference
- Document processing (PDF/TXT)
- Intent detection and entity extraction
- Clean architecture patterns
- Git best practices

---

## 🚀 Next Steps

Want to extend this project? Try:
- [ ] Add authentication (JWT tokens)
- [ ] Implement rate limiting
- [ ] Add support for DOCX, CSV files
- [ ] Multi-document chat (query across multiple docs)
- [ ] Streaming responses
- [ ] Add caching layer
- [ ] Implement user management
- [ ] Deploy to cloud (Railway, Render, AWS)
- [ ] Add monitoring and logging
- [ ] Create a frontend UI

---

## 📝 License

MIT

---

**Built with ❤️ following strict production standards**
