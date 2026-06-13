# 🧪 Manual Test Guide

## ✅ Server is Running!

Your server is now running on **http://localhost:8000**

---

## 📝 Step-by-Step Testing

### Test 1: Health Check

**Open your browser** and go to:
```
http://localhost:8000/
```

You should see:
```json
{
  "status": "online",
  "message": "Conversational RAG Backend API is running",
  "endpoints": ["/ingest", "/chat"]
}
```

---

### Test 2: Open Interactive API Docs

**Go to:**
```
http://localhost:8000/docs
```

This opens Swagger UI where you can test all APIs interactively!

---

### Test 3: Upload Document (Using Swagger UI)

1. On the Swagger page, find **POST /ingest**
2. Click **"Try it out"**
3. Click **"Choose File"** and select `sample_document.txt`
4. Set `strategy` to `sentence`
5. Click **"Execute"**
6. **SAVE the `document_id`** from the response!

---

### Test 4: Chat with Document (Using Swagger UI)

1. Find **POST /chat**
2. Click **"Try it out"**
3. Replace the JSON with (use your document_id):
```json
{
  "session_id": "test-session-1",
  "user_message": "What is machine learning?",
  "document_id": "YOUR_DOCUMENT_ID_HERE"
}
```
4. Click **"Execute"**
5. See the AI response!

---

### Test 5: Test Booking Detection

1. Still on **POST /chat**
2. Use this JSON:
```json
{
  "session_id": "test-session-1",
  "user_message": "I want to book an interview for Alice Smith at alice@example.com on Friday at 3 PM",
  "document_id": "YOUR_DOCUMENT_ID_HERE"
}
```
3. Click **"Execute"**
4. You should see extracted booking information in the response!

---

## 🎯 Success Criteria

✅ Health check returns 200  
✅ Document uploaded successfully  
✅ Got a document_id back  
✅ Chat responds with relevant information  
✅ Booking information extracted correctly  

---

## 💡 Tips

- The **Swagger UI** at `/docs` is the easiest way to test
- Keep the `document_id` handy - you'll need it for chatting
- Use the same `session_id` for related questions to maintain chat history
- Try asking follow-up questions to test chat memory

---

## 🔍 Check Server Logs

The terminal where you ran `python run_server.py` shows:
- Every API request
- Processing steps
- Any errors

---

## ✨ You're Testing a Production-Ready System!

Enjoy exploring your RAG backend! 🚀
