# 📸 Demo Screenshot Guide

## What to Capture

Take screenshots or screen recordings of these 4 scenarios to add to your README or presentation:

---

## 1️⃣ Health Check Response

**Command:**
```bash
curl http://localhost:8000/
```

**What to show:**
- The command in terminal
- The JSON response showing status: "online"

**Screenshot tip:** Capture the full terminal window showing both command and response

---

## 2️⃣ Document Ingestion Success

**Option A: Using curl**
```bash
curl -X POST "http://localhost:8000/ingest?strategy=sentence" \
  -F "file=@sample_document.txt"
```

**Option B: Using Swagger UI** (Recommended - looks better!)
1. Navigate to `http://localhost:8000/docs`
2. Click on `POST /ingest`
3. Click "Try it out"
4. Select `sentence` for strategy
5. Upload `sample_document.txt`
6. Click "Execute"

**What to show:**
- The request details (file name, strategy)
- The successful response with:
  - `document_id`
  - `filename`
  - `chunk_count: 21`
  - `strategy: "sentence"`

**Screenshot tip:** If using Swagger, capture the request section and response section in one screenshot

---

## 3️⃣ Chat Response

**Option A: Using curl**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo-session",
    "user_message": "What is machine learning?",
    "document_id": "YOUR_DOCUMENT_ID_FROM_STEP_2"
  }'
```

**Option B: Using Swagger UI** (Recommended!)
1. Go to `http://localhost:8000/docs`
2. Click on `POST /chat`
3. Click "Try it out"
4. Paste this JSON (replace document_id):
```json
{
  "session_id": "demo-session",
  "user_message": "What is machine learning?",
  "document_id": "6197dd2c-44f1-4456-a0fe-7ec321f10e35"
}
```
5. Click "Execute"

**What to show:**
- The question: "What is machine learning?"
- The response explaining ML with types (supervised, unsupervised, reinforcement)
- `booking: null`

**Screenshot tip:** Show the full response to demonstrate quality of RAG answers

---

## 4️⃣ Booking Detection

**Option A: Using curl**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo-session",
    "user_message": "I want to schedule an interview for Alice Smith at alice@example.com on Friday at 3 PM",
    "document_id": "YOUR_DOCUMENT_ID"
  }'
```

**Option B: Using Swagger UI** (Recommended!)
1. Go to `http://localhost:8000/docs`
2. Click on `POST /chat`
3. Paste this JSON:
```json
{
  "session_id": "demo-session",
  "user_message": "I want to schedule an interview for Alice Smith at alice@example.com on Friday at 3 PM",
  "document_id": "6197dd2c-44f1-4456-a0fe-7ec321f10e35"
}
```
4. Click "Execute"

**What to show:**
- The booking request message
- The response confirming the scheduling
- **MOST IMPORTANT**: The `booking` object with:
  - `name: "Alice Smith"`
  - `email: "alice@example.com"`
  - `date: "Friday"`
  - `time: "3 PM"`

**Screenshot tip:** Highlight or annotate the booking object to draw attention to this feature

---

## 🎥 Video Alternative (Recommended for Presentations!)

Instead of 4 separate screenshots, record a 60-second screen recording showing:

1. Navigate to `http://localhost:8000/docs` (show Swagger UI)
2. Test POST /ingest (upload sample_document.txt)
3. Copy the document_id
4. Test POST /chat with "What is machine learning?"
5. Test POST /chat with booking message
6. Show the booking object in response

**Tools for screen recording:**
- Windows: Xbox Game Bar (Win + G)
- OBS Studio (free)
- ShareX (free)

---

## 📁 Where to Save

Save your screenshots/video as:
- `demo_health_check.png`
- `demo_ingestion.png`
- `demo_chat.png`
- `demo_booking.png`

Or for video:
- `demo_walkthrough.mp4` or `.gif`

---

## 🎨 Pro Tips

1. **Use Swagger UI** - It looks more professional than terminal
2. **Zoom in** - Make text readable (Ctrl + for browser, Ctrl + Mouse Wheel for terminal)
3. **Clean background** - Close unnecessary tabs/windows
4. **Dark mode** - Looks better in presentations (optional)
5. **Annotations** - Use arrows or highlights to point out key parts

---

## 📝 Adding to README

If you want to add screenshots to README, create a `screenshots/` folder:

```bash
mkdir screenshots
# Put your images there
```

Then in README.md, add after each demo section:

```markdown
### 1. Health Check

![Health Check](screenshots/demo_health_check.png)

### 2. Document Ingestion

![Document Ingestion](screenshots/demo_ingestion.png)
```

---

## 🚀 Quick Test Sequence

Before taking screenshots, run this quick sequence to ensure everything works:

```bash
# 1. Start server
python run_server.py

# 2. Health check (new terminal)
curl http://localhost:8000/

# 3. Ingest document
curl -X POST "http://localhost:8000/ingest?strategy=sentence" -F "file=@sample_document.txt"

# 4. Chat (replace document_id with the one from step 3)
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"session_id":"demo","user_message":"What is machine learning?","document_id":"YOUR_ID_HERE"}'

# 5. Booking (replace document_id)
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"session_id":"demo","user_message":"Schedule interview for Alice Smith at alice@test.com Friday 3PM","document_id":"YOUR_ID_HERE"}'
```

If all 5 work, you're ready to take screenshots! 📸
