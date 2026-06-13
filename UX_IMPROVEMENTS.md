# UX Improvements - Session & Chat Management

## Changes Made - June 13, 2026, 01:20 AM

### Issue 1: New Document Upload Should Clear Old Chat ✅

**Problem:** When uploading a new document, old chat messages from previous document remained visible.

**Fix:** 
- Modified `UploadPage.jsx` to call `setMessages([])` when new document is uploaded
- Now: Upload new document → Fresh chat screen

**User Flow:**
1. User chats with document A
2. Clicks "Upload New" → uploads document B
3. Chat clears completely (fresh start for document B)

---

### Issue 2: "New Session" Button Should Clear Chat ✅

**Problem:** "New Session" button only changed session ID but kept all messages visible.

**Fix:**
- Modified `resetSession()` in `AppContext.jsx` to clear messages
- Now: New Session → Fresh chat with new session ID

**User Flow:**
1. User has conversation with multiple messages
2. Clicks "New Session"
3. Session ID changes AND chat clears
4. Can start fresh conversation with same document

---

## Current Behavior Summary

### Upload New Document
- **Triggers:** Clicking "Upload New" button → uploading a document
- **Effect:** 
  - Previous document replaced
  - Chat messages cleared
  - New session ID generated (automatically when page loads)
  - Fresh start

### New Session Button
- **Triggers:** Clicking "New Session" in sidebar
- **Effect:**
  - Session ID changes to new UUID
  - Chat messages cleared
  - Same document remains
  - Fresh conversation with same document

---

## Future Enhancement Ideas

### Chat History Feature (Not Implemented Yet)

**Concept:** Store and display previous chat sessions

**Design:**
```
┌─ Sidebar ─────────────────┐
│ Session Info              │
│  - Current Session ID     │
│  - Document ID            │
│                           │
│ [+ New Session]           │
│                           │
│ ─────────────────────     │
│ Chat History              │
│                           │
│ ● Session abc-123         │
│   3 messages              │
│   2 min ago              │
│                           │
│ ● Session def-456         │
│   8 messages              │
│   1 hour ago             │
│                           │
│ ● Session ghi-789         │
│   5 messages              │
│   Yesterday              │
└───────────────────────────┘
```

**Implementation Approach:**
1. Store sessions in localStorage or backend
2. Each session stores: session_id, messages[], timestamp, document_id
3. Clicking a history item loads that session's messages
4. Current session auto-saves periodically

**Would require:**
- Local storage or backend API for persistence
- Session list component
- Session switching logic
- Timestamp tracking
- Message count display

**Benefits:**
- User can review past conversations
- Better for research/documentation tasks
- Prevents accidental data loss
- Professional multi-session management

---

## Technical Details

### Files Modified
1. `frontend/src/pages/UploadPage.jsx` - Added `setMessages([])` on upload
2. `frontend/src/context/AppContext.jsx` - Modified `resetSession()` to clear messages

### State Management
```javascript
// AppContext state
const [currentDocument, setCurrentDocument] = useState(null);
const [currentSession, setCurrentSession] = useState(() => crypto.randomUUID());
const [messages, setMessages] = useState([]);

// Reset session (clears chat)
const resetSession = () => {
  setCurrentSession(crypto.randomUUID());
  setMessages([]);
};
```

---

## Testing Checklist

### Test 1: Upload New Document Clears Chat
- [ ] Chat with document A, send 3-4 messages
- [ ] Click "Upload New" → upload document B
- [ ] Verify: Chat is completely empty
- [ ] Send message to document B
- [ ] Verify: Only new message appears

### Test 2: New Session Clears Chat
- [ ] Chat with document, send 3-4 messages
- [ ] Click "New Session" button
- [ ] Verify: Session ID changed
- [ ] Verify: Chat is completely empty
- [ ] Send new message
- [ ] Verify: Works with new session ID

---

**Status:** Implemented and ready for testing
**Next:** Consider chat history feature for v2
