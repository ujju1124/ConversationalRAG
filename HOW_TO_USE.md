# 🎯 How to Use Your Conversational RAG Backend

## 📍 You Are Here

Your FastAPI backend is **ready to run**! Here's what to do next:

---

## 🚀 Step 1: Start the Server

Open a terminal in this project directory and run:

```bash
python run_server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open** - the server needs to stay running.

---

## 🌐 Step 2: Open the Interactive Docs

Open your browser and go to:

**http://localhost:8000/docs**

This is Swagger UI - you can test all APIs directly from your browser!

---

## 📤 Step 3: Upload Your First Document

### Option A: Using the Browser (Swagger UI)

1. Go to http://localhost:8000/docs
2. Find the **POST /ingest** endpoint
3. Click **"Try it out"**
4. Choose the file: `sample_document.txt` (included in this project)
5. Select strategy: `sentence`
6. Click **"Execute"**
7. **Copy the `document_id`** from the response - you'll need it!

### Option B: Using curl (Terminal)

Open a **new terminal** (keep the server running) and run:

```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -F "file=@sample_document.txt"
```

**Save the `document_id` from the response!**

---

## 💬 Step 4: Chat with Your Document

### Option A: Using Swagger UI

1. Go to http://localhost:8000/docs
2. Find the **POST /chat** endpoint
3. Click **"Try it out"**
4. Enter this JSON (replace YOUR_DOCUMENT_ID):
```json
{
  "session_id": "my-first-session",
  "user_message": "What is machine learning?",
  "document_id": "YOUR_DOCUMENT_ID"
}
```
5. Click **"Execute"**
6. See the AI response!

### Option B: Using curl

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "my-first-session",
    "user_message": "What is machine learning?",
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

---

## 🎫 Step 5: Test Booking Detection

Try asking to schedule an interview:

```json
{
  "session_id": "my-first-session",
  "user_message": "I want to book an interview for John at john@email.com on Friday at 2 PM",
  "document_id": "YOUR_DOCUMENT_ID"
}
```

The system will automatically detect and extract the booking information!

---

## 🧪 Step 6: Run Automated Tests

We've included a test script that does everything automatically:

```bash
python test_api.py
```

This will:
1. Check if the server is running
2. Upload a document
3. Ask 3 different questions
4. Test booking detection
5. Show you the results

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `run_server.py` | Start the FastAPI server |
| `test_api.py` | Automated testing script |
| `sample_document.txt` | Sample document for testing |
| `.env` | Your API keys (keep secret!) |
| `GETTING_STARTED.md` | Detailed API documentation |
| `README.md` | Full project documentation |
| `PROJECT_SUMMARY.md` | Technical overview |

---

## 🔍 Checking What's Happening

### View Server Logs
Look at the terminal where you ran `python run_server.py` to see:
- API requests being received
- Errors (if any)
- Processing steps

### Check the Database
Your project creates an `app.db` SQLite file with:
- **Documents table**: Uploaded documents metadata
- **Bookings table**: Extracted booking information

View it with any SQLite browser or:
```bash
pip install sqlite-web
sqlite_web app.db
```

### Monitor Redis
Your chat history is stored in Upstash Redis. Check the Upstash dashboard:
https://console.upstash.com/

### Monitor Pinecone
Your vectors are stored in Pinecone. Check the Pinecone dashboard:
https://app.pinecone.io/

---

## 💡 Example Workflow

Here's a complete example:

### 1. Start Server
```bash
python run_server.py
```

### 2. Upload Document (New Terminal)
```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -F "file=@sample_document.txt"
```

Response:
```json
{
  "document_id": "abc-123-xyz",
  "filename": "sample_document.txt",
  "chunk_count": 12,
  "strategy": "sentence"
}
```

### 3. Ask Questions
```bash
# Question 1
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo",
    "user_message": "What are the applications of AI?",
    "document_id": "abc-123-xyz"
  }'

# Question 2 (uses chat history)
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo",
    "user_message": "Can you give me more details?",
    "document_id": "abc-123-xyz"
  }'

# Question 3 (booking intent)
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo",
    "user_message": "I want to schedule an interview for Alice at alice@test.com tomorrow at 3 PM",
    "document_id": "abc-123-xyz"
  }'
```

---

## ⚠️ Troubleshooting

### "Connection refused" error
→ **Server isn't running**. Run `python run_server.py`

### "No relevant context found"
→ **Wrong document_id**. Make sure you're using the ID from the `/ingest` response

### "Pinecone error"
→ **Check your API key** in `.env`. Should start with `pcsk_`

### "Redis error"
→ **Check Redis URL** in `.env`. Should start with `rediss://`

### "Groq API error"
→ **Check API key** in `.env`. Should start with `gsk_`
→ You might have hit rate limits (30 req/min on free tier)

---

## 🎓 What to Try Next

1. **Upload your own documents**
   - PDFs or TXT files
   - Try both `fixed` and `sentence` chunking strategies

2. **Test different questions**
   - Summarization: "Summarize the main points"
   - Specific: "What is NLP?"
   - Contextual: "How does it work?" (uses chat history)

3. **Test booking variations**
   - "Book an interview for NAME at EMAIL"
   - "Schedule a meeting on DATE at TIME"
   - "I'm available WHEN for an appointment"

4. **Try multiple sessions**
   - Use different `session_id` values
   - Each session has independent chat history

5. **Upload multiple documents**
   - Each gets a unique `document_id`
   - Chat with different documents using different IDs

---

## 📚 Learn More

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pinecone Docs**: https://docs.pinecone.io/
- **Groq Docs**: https://console.groq.com/docs
- **Sentence Transformers**: https://www.sbert.net/

---

## 🎉 You're Ready!

Your production-ready RAG backend is fully set up and ready to use.

**Start with**: `python run_server.py`

**Then visit**: http://localhost:8000/docs

Happy building! 🚀
