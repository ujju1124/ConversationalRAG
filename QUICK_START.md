# 🚀 Quick Start Guide

Get the Conversational RAG application running in 5 minutes.

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check Node.js version (need 16+)
node --version

# Check npm
npm --version
```

## Step 1: Environment Setup (2 minutes)

1. **Copy environment template:**
```bash
cp .env.example .env
```

2. **Get API keys** (all free tier):
   - Groq: https://console.groq.com → Create API key
   - Pinecone: https://www.pinecone.io → Create index
   - Upstash Redis: https://upstash.com → Create database

3. **Fill in .env file:**
```env
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=rag-documents
UPSTASH_REDIS_URL=your_redis_url_here
UPSTASH_REDIS_TOKEN=your_redis_token_here
```

## Step 2: Install Dependencies (2 minutes)

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

## Step 3: Start Servers (1 minute)

### Option A: Using Batch Scripts (Windows)

**Terminal 1 - Backend:**
```bash
START_BACKEND.bat
```

**Terminal 2 - Frontend:**
```bash
cd frontend
START_FRONTEND.bat
```

### Option B: Manual Commands

**Terminal 1 - Backend:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Step 4: Access Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Step 5: Test It Out

1. Open http://localhost:5173
2. Drag and drop `sample_document.txt` (included in repo)
3. Select "Sentence Based" strategy
4. Click "Upload Document"
5. Click "Start Chatting"
6. Ask: "What is machine learning?"
7. Try booking: "Schedule interview for John at john@test.com on Monday at 2 PM"

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Install missing packages
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
cd frontend
rmdir /s node_modules
npm install
```

### CORS Error
- Verify backend is running on port 8000
- Check `app/main.py` has CORS configured for localhost:5173

### Upload fails
- Check all API keys in .env are correct
- Verify Pinecone index is created
- Test backend directly at http://localhost:8000/docs

### Chat not working
- Ensure you uploaded a document first
- Check browser console for errors (F12)
- Verify document_id exists in state

## File Locations

**Environment:** `.env` (root)
**Backend:** `app/` folder
**Frontend:** `frontend/` folder
**Sample File:** `sample_document.txt` (root)

## Useful Commands

```bash
# Check backend health
curl http://localhost:8000/

# Test document upload
curl -X POST "http://localhost:8000/ingest?strategy=sentence" -F "file=@sample_document.txt"

# Build frontend for production
cd frontend
npm run build

# Preview production build
npm run preview
```

## Documentation Links

- **Full README:** `README.md`
- **Frontend Guide:** `frontend/README.md`
- **Testing Guide:** `FRONTEND_TESTING_GUIDE.md`
- **Project Status:** `PROJECT_STATUS.md`

## Next Steps

After getting it running:
1. Read `FRONTEND_TESTING_GUIDE.md` for comprehensive testing
2. Try different documents (PDF and TXT)
3. Test booking detection with various formats
4. Check mobile responsive view (F12 → device toolbar)
5. Explore the code structure
6. Record demo for portfolio

## Support

**Issues?**
1. Check error messages in console (F12)
2. Verify all environment variables set
3. Ensure both servers running
4. Check API keys are valid
5. Review FRONTEND_TESTING_GUIDE.md

**Common Fixes:**
- Clear browser cache
- Restart both servers
- Check .env file formatting
- Verify file permissions

---

**Estimated Time:** 5 minutes
**Difficulty:** Easy
**Status:** Production Ready

Happy coding! 🎉
