# 🏗️ System Architecture - Visual Guide

## 📐 HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Postman/curl)                   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ HTTP Requests
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION (main.py)                │
│                     [Swagger Docs at /docs]                     │
└─────────────────────────────────────────────────────────────────┘
                               │
                ┌──────────────┴───────────────┐
                ▼                              ▼
    ┌────────────────────┐          ┌────────────────────┐
    │   POST /ingest     │          │    POST /chat      │
    │  [ingest.py]       │          │    [chat.py]       │
    └────────────────────┘          └────────────────────┘
                │                              │
                │                              │
                ▼                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                     SERVICE LAYER                           │
    ├─────────────────────────────────────────────────────────────┤
    │  • ingestion_service.py  (Extract, Chunk, Embed, Upload)   │
    │  • retrieval_service.py  (Vector Search)                    │
    │  • memory_service.py     (Chat History)                     │
    │  • llm_service.py        (Groq API Calls)                   │
    │  • booking_service.py    (Intent + Extraction)              │
    └─────────────────────────────────────────────────────────────┘
                               │
                ┌──────────────┼───────────────┬──────────────┐
                ▼              ▼               ▼              ▼
        ┌──────────┐    ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Pinecone │    │  Redis   │   │  SQLite  │   │   Groq   │
        │  Vector  │    │  Chat    │   │ Metadata │   │   LLM    │
        │    DB    │    │  Memory  │   │ Bookings │   │   API    │
        └──────────┘    └──────────┘   └──────────┘   └──────────┘
```

---

## 📤 DOCUMENT INGESTION FLOW

```
┌─────────┐
│  User   │
│ Uploads │
│ PDF/TXT │
└────┬────┘
     │
     ▼
┌────────────────────────────────────────┐
│ POST /ingest                           │
│ {file: upload, strategy: "sentence"}  │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│ ingestion_service.process_document()   │
├────────────────────────────────────────┤
│ Step 1: Extract Text                   │
│   ├─ PDF → pdfplumber                  │
│   └─ TXT → read directly               │
│                                        │
│ Step 2: Chunk Text                     │
│   ├─ Fixed: 500 chars, 50 overlap     │
│   └─ Sentence: NLTK tokenization      │
│                                        │
│ Step 3: Generate Embeddings            │
│   └─ all-MiniLM-L6-v2 → 384-dim       │
│                                        │
│ Step 4: Upload to Pinecone             │
│   └─ {vector, metadata: {text,        │
│        document_id, chunk_index}}      │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│ Save Metadata to SQLite                │
│ documents table:                       │
│  - document_id (UUID)                  │
│  - filename                            │
│  - chunk_count                         │
│  - strategy                            │
│  - created_at                          │
└────────────────┬───────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────┐
│ Return Response                        │
│ {                                      │
│   "document_id": "uuid-xxx",           │
│   "filename": "sample.txt",            │
│   "chunk_count": 21,                   │
│   "strategy": "sentence"               │
│ }                                      │
└────────────────────────────────────────┘
```

---

## 💬 CONVERSATIONAL RAG FLOW

```
┌─────────┐
│  User   │
│  Asks   │
│Question │
└────┬────┘
     │
     ▼
┌──────────────────────────────────────────────────────────┐
│ POST /chat                                               │
│ {                                                        │
│   "session_id": "user-123",                             │
│   "user_message": "What is machine learning?",          │
│   "document_id": "uuid-xxx"                             │
│ }                                                        │
└────────────────┬─────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ STEP 1: RETRIEVAL  │
        └────────┬───────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ retrieval_service.retrieve_relevant_chunks()           │
│                                                        │
│ 1. Encode query → 384-dim vector                      │
│ 2. Search Pinecone:                                    │
│    - Filter: {document_id: "uuid-xxx"}               │
│    - Top-K: 5                                          │
│    - Metric: Cosine similarity                        │
│ 3. Extract text from matches                          │
│                                                        │
│ Returns: ["chunk1", "chunk2", ...]                    │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ STEP 2: MEMORY     │
        └────────┬───────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ memory_service.get_chat_history()                      │
│                                                        │
│ 1. Redis key: "chat:user-123"                         │
│ 2. Get last 6 messages                                 │
│                                                        │
│ Returns: [                                             │
│   {"role": "user", "content": "..."},                 │
│   {"role": "assistant", "content": "..."}             │
│ ]                                                      │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ STEP 3: GENERATION │
        └────────┬───────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ llm_service.generate_rag_response()                    │
│                                                        │
│ Build Prompt:                                          │
│ ┌──────────────────────────────────────────┐         │
│ │ Context:                                  │         │
│ │ [1] chunk1 text here...                  │         │
│ │ [2] chunk2 text here...                  │         │
│ │ [3] chunk3 text here...                  │         │
│ │                                           │         │
│ │ Previous Conversation:                    │         │
│ │ User: previous question                   │         │
│ │ Assistant: previous answer                │         │
│ │                                           │         │
│ │ User: What is machine learning?          │         │
│ └──────────────────────────────────────────┘         │
│                                                        │
│ Call Groq API (llama-3.1-8b-instant)                 │
│                                                        │
│ Returns: "Machine learning is..."                     │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ STEP 4: SAVE       │
        └────────┬───────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ memory_service.save_conversation_turn()                │
│                                                        │
│ 1. Save user message to Redis                          │
│ 2. Save assistant response to Redis                    │
│ 3. Set 24-hour expiration                             │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ STEP 5: BOOKING    │
        └────────┬───────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ booking_service.process_booking()                      │
│                                                        │
│ 1. Detect Intent (keyword matching):                   │
│    - Check for: "book", "schedule", "interview"       │
│    - If NO match → return None                        │
│    - If match → continue                              │
│                                                        │
│ 2. Extract Information (LLM):                         │
│    - Prompt: "Extract name, email, date, time..."    │
│    - Call Groq API                                     │
│    - Parse JSON response                              │
│                                                        │
│ 3. Save to Database:                                   │
│    - Insert into bookings table                        │
│    - Return BookingData                                │
│                                                        │
│ Returns: BookingData or None                           │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│ Return Final Response                                  │
│ {                                                      │
│   "response": "Machine learning is...",                │
│   "session_id": "user-123",                           │
│   "booking": {                                         │
│     "name": "Alice",                                   │
│     "email": "alice@example.com",                     │
│     "date": "Friday",                                  │
│     "time": "3 PM"                                     │
│   }                                                    │
│ }                                                      │
└────────────────────────────────────────────────────────┘
```

---

## 🗄️ DATA STORAGE ARCHITECTURE

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│    PINECONE         │  │      REDIS          │  │      SQLITE         │
│  (Vector Search)    │  │   (Session Store)   │  │   (Metadata DB)     │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│                     │  │                     │  │                     │
│ Index: "rag-docs"   │  │ Key Pattern:        │  │ Table: documents    │
│ Dimension: 384      │  │ "chat:{session}"    │  │ ├─ document_id PK   │
│ Metric: cosine      │  │                     │  │ ├─ filename         │
│                     │  │ Data Structure:     │  │ ├─ chunk_count      │
│ Vector Format:      │  │ LIST of JSON        │  │ ├─ strategy         │
│ {                   │  │ [                   │  │ └─ created_at       │
│   id: "uuid-1",     │  │   {                 │  │                     │
│   values: [0.1,..], │  │     "role": "user", │  │ Table: bookings     │
│   metadata: {       │  │     "content": "hi" │  │ ├─ booking_id PK    │
│     document_id,    │  │   },                │  │ ├─ session_id       │
│     text,           │  │   {                 │  │ ├─ name             │
│     chunk_index     │  │     "role": "asst", │  │ ├─ email            │
│   }                 │  │     "content": "..."│  │ ├─ date             │
│ }                   │  │   }                 │  │ ├─ time             │
│                     │  │ ]                   │  │ └─ created_at       │
│ Storage:            │  │                     │  │                     │
│ ✓ Embeddings        │  │ TTL: 24 hours       │  │ Storage:            │
│ ✓ Chunk text        │  │                     │  │ ✓ Doc metadata      │
│ ✓ Document linkage  │  │ Storage:            │  │ ✓ Booking records   │
│                     │  │ ✓ Chat history      │  │                     │
│ Query:              │  │ ✓ Conversation ctx  │  │ File: app.db        │
│ ✓ Semantic search   │  │                     │  │                     │
│ ✓ Filter by doc_id  │  │ Access: O(1)        │  │ Access:             │
│                     │  │ In-memory           │  │ ✓ SQLAlchemy ORM    │
│ Managed Service     │  │                     │  │ ✓ Local file        │
│ Serverless          │  │ Upstash Redis       │  │                     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘

WHY THIS SEPARATION?
• Pinecone: Optimized for vector similarity search
• Redis: Fast temporary storage with TTL
• SQLite: Structured persistent data with relationships
```

---

## 🧩 SERVICE LAYER BREAKDOWN

```
┌─────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                            │
│               (Business Logic - No HTTP Knowledge)              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│ ingestion_service.py │
├──────────────────────┤
│ Functions:           │
│ • extract_text()     │───────► Handles PDF (pdfplumber) + TXT
│ • chunk_fixed()      │───────► 500 chars, 50 overlap
│ • chunk_sentence()   │───────► NLTK punkt tokenizer
│ • generate_emb()     │───────► all-MiniLM-L6-v2 encoding
│ • upload_pinecone()  │───────► Batch upsert to vector DB
│ • process_document() │───────► Main orchestrator
└──────────────────────┘

┌──────────────────────┐
│ retrieval_service.py │
├──────────────────────┤
│ Functions:           │
│ • retrieve_chunks()  │───────► Query Pinecone
│                      │         ├─ Encode query
│                      │         ├─ Filter by doc_id
│                      │         └─ Return top-K chunks
└──────────────────────┘

┌──────────────────────┐
│ memory_service.py    │
├──────────────────────┤
│ Functions:           │
│ • get_history()      │───────► Fetch from Redis
│ • add_message()      │───────► Append to Redis list
│ • save_turn()        │───────► Save user + assistant
└──────────────────────┘

┌──────────────────────┐
│ llm_service.py       │
├──────────────────────┤
│ Functions:           │
│ • call_groq_api()    │───────► Base LLM call
│ • generate_rag()     │───────► Build prompt + call
│                      │         ├─ Format context
│                      │         ├─ Format history
│                      │         └─ Generate response
└──────────────────────┘

┌──────────────────────┐
│ booking_service.py   │
├──────────────────────┤
│ Functions:           │
│ • detect_intent()    │───────► Keyword matching
│ • extract_info()     │───────► LLM extraction
│ • save_booking()     │───────► SQLite insert
│ • process_booking()  │───────► Full flow
└──────────────────────┘
```

---

## 🔄 CHUNKING STRATEGIES COMPARISON

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORIGINAL DOCUMENT                            │
│  "Machine learning is AI. It learns from data. There are       │
│   three types: supervised, unsupervised, and reinforcement."    │
└─────────────────────────────────────────────────────────────────┘
                         │
          ┌──────────────┴───────────────┐
          ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│   FIXED STRATEGY    │      │  SENTENCE STRATEGY  │
│   (500 chars)       │      │   (NLTK-based)      │
└─────────────────────┘      └─────────────────────┘
          │                              │
          ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│ Chunk 1:            │      │ Chunk 1:            │
│ "Machine learn..."  │      │ "Machine learning   │
│ (exactly 500 chars) │      │  is AI."            │
├─────────────────────┤      ├─────────────────────┤
│ Chunk 2:            │      │ Chunk 2:            │
│ "...ning is AI..."  │      │ "It learns from     │
│ (starts at char450) │      │  data."             │
│ [50 char overlap]   │      ├─────────────────────┤
├─────────────────────┤      │ Chunk 3:            │
│ ...                 │      │ "There are three    │
└─────────────────────┘      │  types: supervised, │
                             │  unsupervised, and  │
Pros:                        │  reinforcement."    │
✓ Predictable size           └─────────────────────┘
✓ Fast processing            
✓ Good for long docs         Pros:
                             ✓ Semantic coherence
Cons:                        ✓ Natural boundaries
✗ Breaks sentences           ✓ Better RAG quality
✗ Context fragmentation      
                             Cons:
                             ✗ Variable size
                             ✗ Requires NLTK
```

---

## 🎯 REQUEST/RESPONSE FLOW DIAGRAM

```
CLIENT REQUEST
     │
     │  POST /chat
     │  {
     │    "session_id": "abc",
     │    "user_message": "What is ML?",
     │    "document_id": "xyz"
     │  }
     │
     ▼
┌─────────────────────────────────────┐
│         FastAPI Router              │
│         (chat.py)                   │
│                                     │
│  1. Validate request (Pydantic)     │
│  2. Get DB session                  │
│  3. Call services                   │
│  4. Handle errors                   │
│  5. Return response                 │
└─────────────────────────────────────┘
     │
     ├───► retrieval_service ───► Pinecone (get chunks)
     │
     ├───► memory_service ───► Redis (get history)
     │
     ├───► llm_service ───► Groq API (generate)
     │
     ├───► memory_service ───► Redis (save turn)
     │
     └───► booking_service ───► SQLite (if booking)
           │
           ▼
     ┌─────────────────────────────┐
     │   RESPONSE                  │
     │   {                         │
     │     "response": "ML is...", │
     │     "session_id": "abc",    │
     │     "booking": {...}        │
     │   }                         │
     └─────────────────────────────┘
```

---

## 📦 FOLDER STRUCTURE WITH DEPENDENCIES

```
app/
├── main.py                    [Imports: routers, db]
│
├── core/
│   ├── config.py             [Imports: pydantic_settings]
│   ├── db.py                 [Imports: sqlalchemy, config]
│   ├── pinecone_client.py    [Imports: pinecone, config]
│   └── redis_client.py       [Imports: redis, config]
│
├── models/
│   ├── schemas.py            [Imports: pydantic]
│   └── db_models.py          [Imports: sqlalchemy, db.Base]
│
├── routers/
│   ├── ingest.py             [Imports: FastAPI, services, models, db]
│   └── chat.py               [Imports: FastAPI, services, models, db]
│
└── services/
    ├── ingestion_service.py  [Imports: pdfplumber, sentence_transformers]
    ├── retrieval_service.py  [Imports: sentence_transformers, pinecone]
    ├── memory_service.py     [Imports: redis_client, json]
    ├── llm_service.py        [Imports: groq, config]
    └── booking_service.py    [Imports: llm_service, models, db]

DEPENDENCY FLOW:
main.py → routers → services → core/models
(Top Layer) ↓ ↓ ↓ ↓ (Bottom Layer)
```

---

## 🔐 SECURITY & BEST PRACTICES

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                          │
└─────────────────────────────────────────────────────────────┘

1. ENVIRONMENT VARIABLES
   ├─ All secrets in .env (gitignored)
   ├─ Validated by Pydantic Settings
   └─ Fails fast if keys missing

2. INPUT VALIDATION
   ├─ Pydantic models auto-validate
   ├─ FastAPI returns 422 on bad data
   └─ Type hints everywhere

3. DATABASE SECURITY
   ├─ SQLAlchemy prevents SQL injection
   ├─ UUID primary keys (not sequential IDs)
   └─ Sessions auto-close (context manager)

4. API SECURITY (Production TODOs)
   ├─ Add JWT authentication
   ├─ Rate limiting per user
   ├─ CORS configuration
   └─ HTTPS only

5. DATA ISOLATION
   ├─ document_id filters in Pinecone
   ├─ session_id scopes Redis data
   └─ No cross-user data leakage
```

---

## 📈 SCALABILITY PATHS

```
CURRENT (MVP)              →  PRODUCTION SCALE
─────────────────────────────────────────────────────────

SQLite                     →  PostgreSQL + Connection Pooling
Single server              →  Kubernetes cluster (3+ pods)
No cache                   →  Redis cache for hot chunks
Local embeddings           →  GPU-based embedding service
Synchronous processing     →  Celery task queue for docs
No monitoring              →  Prometheus + Grafana
Manual deployment          →  CI/CD pipeline (GitHub Actions)
Single region              →  Multi-region deployment
No load balancer           →  Nginx/ALB with rate limiting

ESTIMATED CAPACITY:
Current:  ~100 concurrent users
          ~1000 documents
          
Production: ~10,000 concurrent users
            ~1M+ documents
```

---

**Use these diagrams in your interview to visually explain the architecture!**
