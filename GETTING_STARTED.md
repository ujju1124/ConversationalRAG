# 🚀 Getting Started Guide

## Quick Start

### 1. Start the Server

Run the server using either method:

**Method 1: Using the run script**
```bash
python run_server.py
```

**Method 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

---

## 2. Test the APIs

### **Health Check**

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "status": "online",
  "message": "Conversational RAG Backend API is running",
  "endpoints": ["/ingest", "/chat"]
}
```

---

### **API 1: Document Ingestion**

Upload a PDF or TXT file and create vector embeddings.

**Example 1: Upload with sentence chunking**

```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -F "file=@sample_document.pdf"
```

**Example 2: Upload with fixed chunking**

```bash
curl -X POST "http://localhost:8000/ingest?strategy=fixed" \
  -F "file=@readme.txt"
```

**Response:**
```json
{
  "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "sample_document.pdf",
  "chunk_count": 42,
  "strategy": "sentence"
}
```

**Save the `document_id` - you'll need it for chatting!**

---

###  **API 2: Conversational RAG Chat**

Chat with your uploaded document using the document_id.

**Example: Simple question**

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "user_message": "What are the main topics in this document?",
    "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }'
```

**Response:**
```json
{
  "response": "Based on the context provided, the main topics are...",
  "session_id": "user123",
  "booking": null
}
```

**Example: Booking intent detection**

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user456",
    "user_message": "I would like to schedule an interview for John Doe at john@email.com on March 15th at 2 PM",
    "document_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }'
```

**Response with booking:**
```json
{
  "response": "I've noted your interview request...",
  "session_id": "user456",
  "booking": {
    "name": "John Doe",
    "email": "john@email.com",
    "date": "March 15th",
    "time": "2 PM"
  }
}
```

---

## 3. Using Python Requests

### Install requests
```bash
pip install requests
```

### Document Ingestion
```python
import requests

# Upload a document
with open("sample.pdf", "rb") as f:
    files = {"file": f}
    params = {"strategy": "sentence"}
    response = requests.post(
        "http://localhost:8000/ingest",
        files=files,
        params=params
    )
    
result = response.json()
print(f"Document ID: {result['document_id']}")
print(f"Chunks created: {result['chunk_count']}")
```

### Chat with Document
```python
import requests

# Chat with the document
payload = {
    "session_id": "my-session-123",
    "user_message": "Summarize the key points",
    "document_id": "your-document-id-here"
}

response = requests.post(
    "http://localhost:8000/chat",
    json=payload
)

result = response.json()
print(f"Assistant: {result['response']}")

if result['booking']:
    print(f"Booking detected: {result['booking']}")
```

---

## 4. Interactive API Documentation

Visit **http://localhost:8000/docs** to:
- See all available endpoints
- Try APIs directly from your browser
- View request/response schemas
- Download OpenAPI specification

---

## 5. Project Structure Overview

```
app/
├── main.py                 # FastAPI app entry point
├── routers/
│   ├── ingest.py          # POST /ingest endpoint
│   └── chat.py            # POST /chat endpoint
├── services/
│   ├── ingestion_service.py   # Document processing
│   ├── retrieval_service.py   # Vector search
│   ├── memory_service.py      # Chat history (Redis)
│   ├── llm_service.py         # Groq API calls
│   └── booking_service.py     # Booking detection
├── models/
│   ├── schemas.py         # Pydantic models
│   └── db_models.py       # SQLAlchemy models
└── core/
    ├── config.py          # Environment config
    ├── db.py              # Database setup
    ├── pinecone_client.py # Vector DB
    └── redis_client.py    # Chat memory
```

---

## 6. Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify all API keys are set in `.env`
- Run `python -c "from app.main import app; print('OK')"` to test imports

### Pinecone errors
- Verify `PINECONE_API_KEY` is correct
- Ensure `PINECONE_INDEX_NAME` matches your index in Pinecone dashboard
- Check index dimension is 384 (for all-MiniLM-L6-v2)

### Redis errors
- Verify `UPSTASH_REDIS_URL` starts with `rediss://`
- Check `UPSTASH_REDIS_TOKEN` is correct
- Test connection in Upstash dashboard

### Groq API errors
- Verify `GROQ_API_KEY` is valid
- Check rate limits (30 req/min on free tier)
- Ensure model `llama3-8b-8192` is available

---

## 7. What's Next?

- Upload your first document via `/ingest`
- Chat with it via `/chat`
- Try asking booking-related questions
- Explore chat history persistence across sessions
- Check the SQLite database (`app.db`) for stored metadata and bookings

**Happy building! 🎉**
