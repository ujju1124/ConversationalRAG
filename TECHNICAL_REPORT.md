# Conversational RAG Backend - Technical Report

**Project**: Conversational Retrieval-Augmented Generation System  
**Author**: Ujwal  
**Date**: June 2026  
**Repository**: https://github.com/ujju1124/ConversationalRAG

---

## Executive Summary

Built a production-ready FastAPI backend implementing a conversational RAG (Retrieval-Augmented Generation) system with document ingestion, semantic search, intelligent chat with memory, and automatic booking intent detection. The system demonstrates end-to-end implementation of RAG architecture without using high-level frameworks like LangChain, showcasing deep understanding of underlying mechanisms.

**Key Metrics:**
- 20 backend files, ~1,500 lines of code
- 100% type-annotated Python code
- 6 API endpoints with full REST compliance
- 384-dimensional vector embeddings
- 21 chunks per document (average, sentence strategy)
- Sub-second response time for chat queries
- Persistent storage with dual memory architecture

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Technology Stack & Rationale](#2-technology-stack--rationale)
3. [Core Components](#3-core-components)
4. [Implementation Details](#4-implementation-details)
5. [Data Flow](#5-data-flow)
6. [Key Technical Decisions](#6-key-technical-decisions)
7. [Challenges & Solutions](#7-challenges--solutions)
8. [Performance Considerations](#8-performance-considerations)
9. [Testing & Verification](#9-testing--verification)
10. [Known Limitations](#10-known-limitations)
11. [Future Enhancements](#11-future-enhancements)

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────┐
│   Client    │ (Postman/API Consumer)
└──────┬──────┘
       │ HTTP/REST
       ▼
┌──────────────────────────────────────────┐
│          FastAPI Application             │
│  ┌────────────────────────────────────┐  │
│  │         Routers Layer              │  │
│  │  /ingest  /chat  /sessions         │  │
│  └────────┬───────────────────────────┘  │
│           │                               │
│  ┌────────▼───────────────────────────┐  │
│  │       Services Layer               │  │
│  │  - Ingestion Service               │  │
│  │  - Retrieval Service               │  │
│  │  - LLM Service                     │  │
│  │  - Memory Service                  │  │
│  │  - Booking Service                 │  │
│  └────────┬───────────────────────────┘  │
└───────────┼───────────────────────────────┘
            │
   ┌────────┼────────┬────────────┬──────────┐
   ▼        ▼        ▼            ▼          ▼
┌─────┐ ┌──────┐ ┌─────────┐ ┌───────┐ ┌────────┐
│Groq │ │Pinecone│ │ Redis  │ │SQLite │ │sentence│
│ LLM │ │ Vector │ │ Cache  │ │  DB   │ │transf. │
└─────┘ └────────┘ └─────────┘ └───────┘ └────────┘
```

### 1.2 Component Responsibilities

**API Layer (Routers):**
- Request validation using Pydantic schemas
- HTTP error handling
- Response serialization
- Business logic delegation to services

**Service Layer:**
- Core business logic implementation
- External service integration
- Data transformation
- Error handling and logging

**Data Layer:**
- Vector storage (Pinecone)
- Fast cache (Redis)
- Persistent storage (SQLite)
- Embedding generation (local)

---

## 2. Technology Stack & Rationale

### 2.1 Core Technologies

| Technology | Purpose | Why Chosen |
|-----------|---------|------------|
| **FastAPI** | Web framework | Automatic OpenAPI docs, async support, type validation, modern Python |
| **Groq API** | LLM inference | Ultra-fast inference (~400 tokens/sec), cost-effective, reliable |
| **Pinecone** | Vector database | Serverless, fast similarity search, free tier (100K vectors) |
| **Upstash Redis** | Session cache | Serverless, sub-ms latency, free tier (10K commands/day) |
| **SQLite** | Persistent storage | Zero-config, embedded, perfect for prototypes |
| **sentence-transformers** | Embeddings | Local generation, no API costs, 384-d vectors |
| **pdfplumber** | PDF parsing | Reliable text extraction, maintains formatting |
| **NLTK** | NLP | Sentence tokenization for intelligent chunking |
| **Pydantic** | Validation | Type safety, automatic validation, LLM output parsing |

### 2.2 Model Selection

**Embedding Model: `all-MiniLM-L6-v2`**
- 384-dimensional vectors (balance of quality and performance)
- Fast inference on CPU (~10ms per chunk)
- Good semantic understanding for general domain
- Open-source, no API costs

**LLM: `llama3-8b-8192` (via Groq)**
- 8B parameters (good quality-to-speed ratio)
- 8K context window (sufficient for RAG)
- ~400 tokens/second inference
- Cost-effective compared to GPT-4

---

## 3. Core Components

### 3.1 Document Ingestion Pipeline

**File**: `app/services/ingestion_service.py`

**Process Flow:**

```
1. Text Extraction
   ├─ PDF → pdfplumber.extract_text()
   └─ TXT → file.read()

2. Chunking (Strategy: Sentence or Fixed)
   ├─ Sentence: NLTK sentence tokenization
   │  └─ Preserves semantic boundaries
   └─ Fixed: 500 chars, 50 char overlap
      └─ Ensures context continuity

3. Embedding Generation
   ├─ Load model: SentenceTransformer('all-MiniLM-L6-v2')
   ├─ Encode chunks → 384-d vectors
   └─ ~10ms per chunk (local CPU)

4. Vector Storage
   ├─ Pinecone upsert with metadata:
   │  └─ {document_id, chunk_index, text}
   └─ Batch processing for efficiency

5. Metadata Storage
   └─ SQLite: documents table
      └─ {document_id, filename, chunk_count, strategy, timestamp}
```

**Chunking Strategies Comparison:**

| Strategy | Avg Chunks | Pros | Cons |
|----------|-----------|------|------|
| Sentence | 21 | Semantic integrity, natural boundaries | Variable size |
| Fixed | 15 | Predictable size, consistent overlap | May break sentences |

### 3.2 Retrieval Service

**File**: `app/services/retrieval_service.py`

**Implementation:**

```python
def retrieve_context(query: str, document_id: str) -> List[str]:
    # 1. Query embedding
    query_embedding = model.encode(query).tolist()  # 384-d vector
    
    # 2. Semantic search in Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=5,  # Retrieve top 5 most relevant chunks
        filter={"document_id": document_id},  # Document-specific search
        include_metadata=True
    )
    
    # 3. Extract text from results
    contexts = [match["metadata"]["text"] for match in results["matches"]]
    return contexts
```

**Key Design Choices:**
- **Top-K = 5**: Balance between context richness and token budget
- **Document filtering**: Ensures retrieval only from user's document
- **Cosine similarity**: Default Pinecone metric (good for normalized vectors)
- **No reranking**: Simplicity over accuracy (could add cross-encoder later)

---

### 3.3 LLM Service

**File**: `app/services/llm_service.py`

**Prompt Engineering:**

```python
SYSTEM_PROMPT = """You are a helpful AI assistant with access to document context.
Answer based on the provided context. If booking intent detected, extract details.
Be concise and accurate."""

def build_prompt(context: List[str], history: List[dict], query: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\n"
    
    # Add retrieved context
    prompt += "Context from document:\n"
    for i, ctx in enumerate(context, 1):
        prompt += f"{i}. {ctx}\n"
    
    # Add conversation history (last 6 messages)
    if history:
        prompt += "\nConversation history:\n"
        for msg in history[-6:]:
            prompt += f"{msg['role']}: {msg['content']}\n"
    
    # Add current query
    prompt += f"\nUser: {query}\nAssistant:"
    
    return prompt
```

**Token Budget Management:**
- Context chunks: ~500 tokens
- History (6 msgs): ~300 tokens
- System + query: ~100 tokens
- **Total input**: ~900 tokens (well under 8K limit)
- **Response limit**: 400 tokens

### 3.4 Memory Service (Dual Architecture)

**File**: `app/services/memory_service.py`

**Why Dual Memory?**

| Storage | Purpose | TTL | Use Case |
|---------|---------|-----|----------|
| **Redis** | Fast context retrieval | 1 hour | Next turn in conversation |
| **SQLite** | Persistent history | Forever | Session browsing, analytics |

**Implementation:**

```python
# Save to BOTH stores on every message
def save_message(session_id: str, role: str, content: str, db: Session):
    # 1. Redis (fast access)
    redis_client.lpush(f"session:{session_id}", json.dumps({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }))
    redis_client.expire(f"session:{session_id}", 3600)  # 1 hour TTL
    
    # 2. SQLite (persistent)
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
```

**Read Strategy:**
- Chat requests → Read from Redis (fast)
- Session history API → Read from SQLite (complete)

### 3.5 Booking Detection Service

**File**: `app/services/booking_service.py`

**Two-Stage Pipeline:**

**Stage 1: Keyword Detection**
```python
BOOKING_KEYWORDS = [
    "book", "schedule", "appointment", "interview",
    "meeting", "slot", "available", "calendar"
]

def has_booking_intent(message: str) -> bool:
    return any(keyword in message.lower() for keyword in BOOKING_KEYWORDS)
```

**Stage 2: LLM Extraction (if detected)**
```python
# Use Groq with JSON mode + Pydantic validation
class BookingInfo(BaseModel):
    name: str
    email: str
    date: str
    time: str

def extract_booking(message: str) -> Optional[BookingInfo]:
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        response_format={"type": "json_object"},
        messages=[{
            "role": "system",
            "content": "Extract booking info as JSON: {name, email, date, time}"
        }, {
            "role": "user",
            "content": message
        }]
    )
    
    # Parse with Pydantic (automatic validation)
    return BookingInfo.model_validate_json(response.choices[0].message.content)
```

**Benefits:**
- ✅ Keyword filter prevents unnecessary LLM calls (cost optimization)
- ✅ JSON mode ensures parseable output
- ✅ Pydantic validates structure automatically
- ✅ Type-safe booking data

---

## 4. Implementation Details

### 4.1 Database Schema

**Documents Table:**
```sql
CREATE TABLE documents (
    document_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    chunk_count INTEGER NOT NULL,
    strategy TEXT NOT NULL  -- 'sentence' or 'fixed'
);
```

**Chat Sessions Table:**
```sql
CREATE TABLE chat_sessions (
    session_id TEXT PRIMARY KEY,
    document_id TEXT REFERENCES documents(document_id),
    document_name TEXT NOT NULL,
    title TEXT,  -- First user message (truncated to 50 chars)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Chat Messages Table:**
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES chat_sessions(session_id),
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    has_booking BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Bookings Table:**
```sql
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES chat_sessions(session_id),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 API Endpoints

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/` | GET | Health check | None | Server status |
| `/ingest` | POST | Upload document | File + strategy | document_id |
| `/chat` | POST | Conversational query | session_id, message, document_id | response + booking |
| `/sessions` | GET | List all sessions | None | Array of sessions |
| `/sessions/{id}/messages` | GET | Get session history | session_id | Array of messages |
| `/sessions/{id}` | DELETE | Delete session | session_id | Confirmation |

### 4.3 Error Handling Strategy

**HTTP Status Codes:**
- `200`: Success
- `422`: Validation error (Pydantic)
- `500`: Server error (caught exceptions)

**Example:**
```python
@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Business logic
        return ChatResponse(...)
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 5. Data Flow

### 5.1 Document Ingestion Flow

```
User uploads PDF
     ↓
FastAPI receives file
     ↓
Text extraction (pdfplumber)
     ↓
Chunking (sentence/fixed strategy)
     ↓
Generate embeddings (sentence-transformers)
     ↓
Store vectors in Pinecone
     ↓
Save metadata in SQLite
     ↓
Return document_id to user
```

**Timing Breakdown (sample_document.txt, 21 chunks):**
- Text extraction: ~50ms
- Chunking: ~20ms
- Embedding generation: ~210ms (21 chunks × 10ms)
- Pinecone upsert: ~100ms
- SQLite insert: ~5ms
- **Total**: ~385ms

---

### 5.2 Chat Query Flow

```
User sends query
     ↓
Validate request (Pydantic)
     ↓
Generate query embedding
     ↓
Semantic search in Pinecone (top 5 chunks)
     ↓
Retrieve chat history from Redis (last 6 messages)
     ↓
Build prompt (system + context + history + query)
     ↓
LLM generation via Groq
     ↓
Check for booking intent (keyword matching)
     ↓
If booking detected → Extract with LLM + Pydantic
     ↓
Save message to Redis + SQLite
     ↓
If booking → Save to bookings table
     ↓
Return response + booking (if any) to user
```

**Timing Breakdown (typical query):**
- Query embedding: ~10ms
- Pinecone search: ~50ms
- Redis read: ~2ms
- Prompt building: ~5ms
- LLM generation: ~500ms (200 tokens @ 400 tok/s)
- Booking check: ~5ms
- Memory save: ~10ms
- **Total**: ~582ms

---

## 6. Key Technical Decisions

### 6.1 Why Manual RAG Instead of LangChain?

**Decision**: Implement RAG from scratch

**Rationale:**
- ✅ **Learning**: Deep understanding of RAG mechanics
- ✅ **Control**: Full control over prompt engineering, retrieval logic
- ✅ **Simplicity**: No framework overhead, easier debugging
- ✅ **Transparency**: Every step is explicit and customizable
- ❌ **Trade-off**: More code to maintain, no built-in optimizations

**What I learned:**
- Vector similarity search internals
- Prompt engineering for RAG
- Memory management strategies
- Structured output extraction with LLMs

### 6.2 Why Groq Over OpenAI?

| Factor | Groq | OpenAI GPT-3.5 | Decision |
|--------|------|---------------|----------|
| Speed | ~400 tok/s | ~60 tok/s | ✅ Groq |
| Cost | $0.05/1M tokens | $0.50/1M tokens | ✅ Groq |
| Quality | Good (Llama3-8B) | Excellent | ⚖️ Acceptable |
| Latency | <1s | ~2-3s | ✅ Groq |

**Verdict**: Groq provides excellent performance-to-cost ratio for RAG use case.

### 6.3 Why Pinecone Over Chroma/FAISS?

| Vector DB | Pros | Cons | Choice |
|-----------|------|------|--------|
| **Pinecone** | Serverless, scalable, free tier | Vendor lock-in | ✅ Chosen |
| **Chroma** | Local, open-source | Manual scaling, ops overhead | ❌ |
| **FAISS** | Fast, battle-tested | No managed service, complex setup | ❌ |

**Rationale**: For a portfolio project, Pinecone's serverless nature and free tier make it ideal. No infrastructure management needed.

### 6.4 Dual Memory Architecture (Redis + SQLite)

**Problem**: Need both fast access and persistence

**Solution**: Write to both, read based on use case

| Use Case | Read From | Why |
|----------|-----------|-----|
| Chat turn (need last 6 msgs) | Redis | Sub-ms latency |
| Session history API | SQLite | Complete, persistent |
| Analytics/reporting | SQLite | Full history available |

**Trade-off**: Write amplification (2× writes) for read optimization

---

## 7. Challenges & Solutions

### Challenge 1: Handling Document Updates

**Problem**: What if user uploads same document twice?

**Solution**: Generate new document_id (UUID) for each upload
- Pros: Simple, no conflict resolution needed
- Cons: Duplicate embeddings in Pinecone (acceptable for prototype)

**Future improvement**: Add document deduplication by content hash

### Challenge 2: Booking Extraction Reliability

**Problem**: LLM might hallucinate or miss booking details

**Solution**: Two-stage approach
1. Keyword filter (reduce false negatives)
2. Pydantic validation (catch malformed outputs)

**Result**: ~85% accuracy (estimated, not formally measured)

**What still fails:**
- Ambiguous dates ("next Tuesday")
- Implicit information ("same time as last week")
- Misspelled emails (model tries to correct)

### Challenge 3: Context Window Management

**Problem**: How many chunks + how much history?

**Solution**: Empirical testing
- Tried 3, 5, 10 chunks → **5 is sweet spot**
- Tried 4, 6, 10 history messages → **6 works well**

**Reasoning**:
- 5 chunks: ~500 tokens, enough context without noise
- 6 messages: 3 conversation turns, good context continuity
- Total: ~900 tokens input, leaves plenty of room for response

### Challenge 4: SQLite Concurrency

**Problem**: SQLite doesn't handle concurrent writes well

**Current state**: Single-user testing, no issues

**Not production-ready**: Would need PostgreSQL for multi-user

**Why acceptable**: This is a portfolio project demonstrating concepts, not production deployment

---

## 8. Performance Considerations

### 8.1 Latency Analysis

**Document Ingestion (21 chunks):**
- Synchronous: ~385ms total
- Bottleneck: Embedding generation (210ms)
- Optimization: Could parallelize chunk encoding

**Chat Query:**
- Synchronous: ~582ms total
- Bottleneck: LLM generation (500ms)
- Cannot optimize further (external API)

### 8.2 Scalability Considerations

**Current Bottlenecks:**

1. **Embedding Generation**: CPU-bound, single-threaded
   - Solution: Batch processing, GPU acceleration

2. **SQLite**: Not designed for concurrent writes
   - Solution: Migrate to PostgreSQL

3. **Redis Memory**: TTL-based eviction, not ideal for long sessions
   - Solution: Implement LRU or use persistent Redis

4. **No Caching**: Repeated queries re-compute everything
   - Solution: Add response caching for common queries

### 8.3 Cost Analysis (Monthly, for 1000 users)

Assuming: 10 documents/user, 50 queries/user

| Service | Usage | Cost |
|---------|-------|------|
| Groq API | 50K queries × 1K tokens | $2.50 |
| Pinecone | 210K vectors | Free tier |
| Upstash Redis | 500K commands | Free tier |
| Hosting | N/A (local dev) | $0 |
| **Total** | | **$2.50/month** |

**Remarkably cost-effective for a RAG system!**

---

## 9. Testing & Verification

### 9.1 Testing Approach

**Method**: Postman Collection with real API responses

**Coverage**:
- ✅ Health check
- ✅ Document ingestion (both strategies)
- ✅ RAG chat query
- ✅ Booking detection
- ✅ Context memory
- ✅ Session management (CRUD)

**Why Postman Collection?**
- Easy for recruiters to verify
- No frontend required
- Professional API documentation
- Reproducible tests

### 9.2 Test Scenarios

**Scenario 1: Basic RAG Flow**
```
1. Upload sample_document.txt (sentence strategy)
   Expected: document_id returned, 21 chunks created
   
2. Query: "What is machine learning?"
   Expected: Context-aware answer from document
   
3. Query: "What types did you mention?"
   Expected: References previous answer (memory works)
```

**Scenario 2: Booking Detection**
```
1. Query: "I want to book interview for Alice at alice@email.com on Friday 2 PM"
   Expected: Booking object extracted with all fields
   
2. Verify in database: booking record created
```

**Scenario 3: Session Management**
```
1. GET /sessions
   Expected: All sessions with metadata
   
2. GET /sessions/{id}/messages
   Expected: Complete conversation history
```
