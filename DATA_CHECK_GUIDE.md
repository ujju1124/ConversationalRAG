# 📊 Data Check Guide

Complete guide to viewing all data stored by your RAG system.

---

## 🗄️ **1. SQLite Database (app.db)**

### **Quick Check (Python)**
```bash
python view_database.py
```

### **Your Current Data:**
```
📄 DOCUMENTS TABLE
- Document ID: 6197dd2c-44f1-4456-a0fe-7ec321f10e35
- Filename: sample_document.txt
- Upload Time: 2026-06-09 16:21:36
- Chunk Count: 21 chunks
- Strategy: sentence

📅 BOOKINGS TABLE  
- Booking ID: a1be3e72-006f-4a78-8be3-c3b22ae68a24
- Session ID: my-first-chat
- Name: Alice Smith
- Email: alice@example.com
- Date: Friday
- Time: 3 PM
- Created At: 2026-06-09 16:28:13
```

### **Using DB Browser (Optional)**
1. Download: https://sqlitebrowser.org/
2. Open `app.db`
3. Browse tables: `documents` and `bookings`

---

## 🔴 **2. Redis (Chat History)**

### **Quick Check (Python)**
```bash
python view_redis.py
```

### **Your Current Data:**
```
💬 SESSION: my-first-chat
Messages: 6

1. 👤 USER: What is machine learning?
2. 🤖 ASSISTANT: Machine learning is a subset of AI...

3. 👤 USER: What are its main types?
4. 🤖 ASSISTANT: There are three main types: supervised learning...

5. 👤 USER: I'd like to schedule an interview for Alice Smith...
6. 🤖 ASSISTANT: Interview has been scheduled for Alice Smith...
```

### **Check via Upstash Dashboard**
1. Go to: https://console.upstash.com/
2. Click on your Redis database
3. Go to "Data Browser" tab
4. Look for keys starting with `chat:`

---

## 📌 **3. Pinecone (Vector Embeddings)**

### **Quick Stats**
```bash
python view_pinecone.py
```

### **Your Current Data:**
```
📌 INDEX: conversational-rag
- Total Vectors: 21 vectors
- Dimension: 384 (all-MiniLM-L6-v2)
- Each vector represents one sentence chunk from your document
```

### **Check via Pinecone Dashboard**
1. Go to: https://app.pinecone.io/
2. Click on your index: `conversational-rag`
3. View stats and vectors
4. You can see vector IDs, metadata, and perform queries

---

## 🔍 **Manual SQL Queries**

### **View All Documents**
```bash
python -c "import sqlite3; conn = sqlite3.connect('app.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM documents'); print(cursor.fetchall())"
```

### **View All Bookings**
```bash
python -c "import sqlite3; conn = sqlite3.connect('app.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM bookings'); print(cursor.fetchall())"
```

### **Count Total Bookings**
```bash
python -c "import sqlite3; conn = sqlite3.connect('app.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM bookings'); print('Total bookings:', cursor.fetchone()[0])"
```

---

## 📈 **Data Flow Visualization**

```
User uploads document
        ↓
[Text Extraction] → sample_document.txt content
        ↓
[Chunking] → 21 sentence chunks
        ↓
[Embedding] → 21 × 384-dimensional vectors
        ↓
[Pinecone] ✅ Stored as searchable vectors
        ↓
[SQLite] ✅ Metadata saved
        
---

User sends chat message
        ↓
[Redis] ← Fetch last 6 messages
        ↓
[Embedding] → Convert message to vector
        ↓
[Pinecone] → Find 5 most similar chunks
        ↓
[Groq LLM] → Generate response with context
        ↓
[Redis] ✅ Save conversation turn
        ↓
[Booking Detection] → Check for booking intent
        ↓
[SQLite] ✅ Save booking if detected
```

---

## 🎯 **Data Retention**

| Storage | Retention | Notes |
|---------|-----------|-------|
| **Pinecone** | Permanent | Vectors stay until deleted |
| **Redis** | 24 hours | Auto-expires after 1 day |
| **SQLite** | Permanent | Local file, persists forever |

---

## 🧹 **Cleanup Commands**

### **Clear All Redis Data**
```python
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()
client = Redis.from_url(
    os.getenv('UPSTASH_REDIS_URL'),
    password=os.getenv('UPSTASH_REDIS_TOKEN'),
    decode_responses=True
)
keys = client.keys('chat:*')
for key in keys:
    client.delete(key)
print(f"Deleted {len(keys)} sessions")
```

### **Clear All Pinecone Vectors**
```python
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index(os.getenv('PINECONE_INDEX_NAME'))
index.delete(delete_all=True)
print("All vectors deleted")
```

### **Clear SQLite Database**
```bash
# Delete the database file
rm app.db

# Or clear tables
python -c "import sqlite3; conn = sqlite3.connect('app.db'); conn.execute('DELETE FROM documents'); conn.execute('DELETE FROM bookings'); conn.commit(); print('Tables cleared')"
```

---

## 📊 **Summary of Your Current Data**

✅ **Pinecone**: 21 vector chunks (384-dimensional)  
✅ **Redis**: 1 session with 6 messages  
✅ **SQLite**: 1 document + 1 booking  

**Total Storage Used:**
- Pinecone: ~8KB (21 vectors × 384 dimensions × 4 bytes)
- Redis: ~500 bytes (chat history)
- SQLite: ~4KB (metadata + booking)

**Total: ~12KB** - Very efficient! 🎉

---

## 🔗 **Online Dashboards**

1. **Pinecone**: https://app.pinecone.io/
2. **Upstash Redis**: https://console.upstash.com/
3. **Groq**: https://console.groq.com/

You can view all your data directly in these dashboards too!

---

**Need to check specific data? Run the Python scripts above!** 🚀
