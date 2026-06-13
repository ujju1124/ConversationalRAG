# Frontend Testing Guide

Complete guide to test the React frontend with the backend.

## Prerequisites

✅ Backend running on `http://localhost:8000`
✅ Frontend running on `http://localhost:5173`

## Starting Both Servers

### Terminal 1 - Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

## Test Scenarios

### 1. Upload Page Tests

#### Test 1.1: Drag and Drop Upload
1. Open `http://localhost:5173` in browser
2. Drag `sample_document.txt` to the upload zone
3. **Expected**: File name and size displayed
4. Select "Sentence Based" strategy
5. Click "Upload Document"
6. **Expected**: 
   - Loading spinner appears
   - Success message with document details
   - "Start Chatting" button appears

#### Test 1.2: Click to Browse Upload
1. Refresh page
2. Click on upload zone
3. Select a PDF or TXT file from file dialog
4. **Expected**: File name appears
5. Select "Fixed Size" strategy
6. Click "Upload Document"
7. **Expected**: Success with document ID displayed

#### Test 1.3: Invalid File Type
1. Try to upload a .jpg or .png file
2. **Expected**: Error toast "Only PDF and TXT files are allowed"

#### Test 1.4: Copy Document ID
1. After successful upload, click copy button next to document ID
2. **Expected**: Toast "Document ID copied!"
3. Paste in notepad to verify

### 2. Chat Page Tests

#### Test 2.1: Navigation from Upload Page
1. Upload a document successfully
2. Click "Start Chatting" button
3. **Expected**: 
   - Navigates to `/chat`
   - Document name shows in navbar
   - Session ID visible in sidebar

#### Test 2.2: Send Message
1. Type "What is machine learning?" in input box
2. Press Enter
3. **Expected**:
   - Message appears on right (user bubble)
   - Typing indicator shows (three dots)
   - Response appears on left (assistant bubble)
   - Input clears after sending

#### Test 2.3: Multi-line Message
1. Type "Tell me about" then press Shift+Enter
2. Type "neural networks"
3. Press Enter
4. **Expected**: Multi-line message sent correctly

#### Test 2.4: Character Count
1. Type a long message
2. **Expected**: Character count updates (e.g., "250/1000")

#### Test 2.5: Message History
1. Send 3-4 messages
2. Scroll up to see previous messages
3. Send a new message
4. **Expected**: Auto-scrolls to latest message

### 3. Booking Detection Tests

#### Test 3.1: Full Booking Information
1. Send message: "I want to schedule an interview for John Doe at john@example.com on Monday at 2 PM"
2. **Expected**:
   - Assistant response acknowledges booking
   - Green booking card appears below response
   - Card shows: Name, Email, Date, Time
   - "Booking Confirmed" badge with checkmark

#### Test 3.2: Partial Booking Information
1. Send message: "Book interview for Alice Smith on Friday at 3 PM"
2. **Expected**:
   - Response asks for missing email
   - Booking card shows available info
   - Missing fields show as "Not provided"

#### Test 3.3: No Booking Information
1. Send message: "Explain deep learning"
2. **Expected**:
   - Normal response, no booking card
   - `booking: null` in response

### 4. Sidebar Tests

#### Test 4.1: Copy Session ID
1. Click copy button next to Session ID
2. **Expected**: Toast "Session ID copied!"
3. Verify by pasting

#### Test 4.2: Copy Document ID
1. Click copy button next to Document ID
2. **Expected**: Toast "Document ID copied!"

#### Test 4.3: New Session Button
1. Click "New Session" button
2. **Expected**:
   - Session ID changes
   - Chat history clears
   - Document ID remains same

#### Test 4.4: Upload New Button
1. Click "Upload New" in navbar
2. **Expected**: Redirects to `/` (upload page)

### 5. Responsive Design Tests

#### Test 5.1: Mobile View
1. Open browser dev tools (F12)
2. Toggle device toolbar (iPhone/Android view)
3. **Expected**:
   - Sidebar collapses to hamburger menu
   - Chat bubbles stack properly
   - Input box remains at bottom
   - All buttons accessible

#### Test 5.2: Tablet View
1. Set viewport to tablet size (768px)
2. **Expected**: Layout adjusts appropriately

### 6. Error Handling Tests

#### Test 6.1: Backend Down
1. Stop backend server
2. Try to upload document
3. **Expected**: Error toast with connection error message

#### Test 6.2: Chat Without Document
1. Manually navigate to `http://localhost:5173/chat`
2. **Expected**: Redirects to upload page

#### Test 6.3: Invalid Document ID
1. In AppContext, manually set invalid document_id
2. Try to send chat message
3. **Expected**: Error toast with API error

#### Test 6.4: Network Timeout
1. Throttle network in dev tools (Slow 3G)
2. Upload large PDF
3. **Expected**: Loading spinner shows, eventually succeeds or times out gracefully

### 7. Toast Notification Tests

#### Test 7.1: Success Toast
1. Upload document successfully
2. **Expected**: Green success toast, auto-dismisses after 3 seconds

#### Test 7.2: Error Toast
1. Trigger any error (invalid file, backend down)
2. **Expected**: Red error toast, auto-dismisses after 3 seconds

#### Test 7.3: Info Toast
1. Copy document ID or session ID
2. **Expected**: Blue info toast, auto-dismisses after 3 seconds

### 8. Animation Tests

#### Test 8.1: Page Transitions
1. Navigate between pages
2. **Expected**: Smooth fade-in animations

#### Test 8.2: Message Animations
1. Send new message
2. **Expected**: Fade-in-up animation on message appearance

#### Test 8.3: Typing Indicator
1. Send message, watch typing indicator
2. **Expected**: Three dots bounce smoothly

### 9. State Persistence Tests

#### Test 9.1: Session Persistence
1. Upload document, start chatting
2. Send 2-3 messages
3. Click "Upload New" then browser back button
4. **Expected**: Chat history still visible

#### Test 9.2: Page Refresh
1. Chat with document
2. Refresh page (F5)
3. **Expected**: Session resets, need to re-upload

### 10. Edge Cases

#### Test 10.1: Empty Message
1. Click send without typing anything
2. **Expected**: Nothing happens (button disabled or validation)

#### Test 10.2: Very Long Message
1. Type 2000+ character message
2. **Expected**: Character count shows, sends successfully

#### Test 10.3: Rapid Consecutive Messages
1. Send 5 messages quickly one after another
2. **Expected**: All messages queued and handled properly

#### Test 10.4: Special Characters in Message
1. Send message with emojis, symbols: "🚀 Test @#$%"
2. **Expected**: Renders correctly in chat bubble

## Browser Compatibility

Test in multiple browsers:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Edge (latest)
- ✅ Safari (if on Mac)

## Performance Checks

### Load Time
- Initial page load should be < 2 seconds
- Document upload should show immediate feedback
- Chat responses should appear within 3-5 seconds

### Smooth Animations
- No jank or stuttering in animations
- Smooth scrolling in chat window
- Responsive button interactions

## Checklist Summary

**Upload Page:**
- [ ] Drag and drop works
- [ ] File browser works
- [ ] Both strategies selectable
- [ ] Success state displays correctly
- [ ] Document ID copyable
- [ ] Navigation to chat works

**Chat Page:**
- [ ] Messages send and display correctly
- [ ] Typing indicator shows
- [ ] Auto-scroll works
- [ ] Booking cards display
- [ ] Sidebar toggles on mobile
- [ ] Copy buttons work
- [ ] New session resets correctly

**Error Handling:**
- [ ] Invalid file types rejected
- [ ] Backend errors shown in toast
- [ ] Network errors handled gracefully
- [ ] Redirect to upload if no document

**UI/UX:**
- [ ] Dark theme applied throughout
- [ ] Glassmorphism effects visible
- [ ] Animations smooth
- [ ] Responsive on all screen sizes
- [ ] Toasts auto-dismiss

## Common Issues & Solutions

**Issue**: CORS error in console
**Solution**: Verify backend CORS config includes `http://localhost:5173`

**Issue**: "Cannot read property of undefined"
**Solution**: Check AppContext is wrapping the app in `main.jsx`

**Issue**: Styles not applying
**Solution**: Ensure Tailwind is configured correctly, check `tailwind.config.js`

**Issue**: API calls failing
**Solution**: Verify backend is running on port 8000

**Issue**: Blank page
**Solution**: Check browser console for errors, verify all imports

## Final Verification

Before considering the frontend complete:

1. ✅ All 10 test scenarios pass
2. ✅ No console errors or warnings
3. ✅ All animations smooth
4. ✅ Mobile responsive
5. ✅ Error states handled
6. ✅ Documentation complete
7. ✅ Code is clean (no console.logs, unused imports)

## Recording Demo

For portfolio purposes, record:
1. Document upload process (both strategies)
2. Chat interaction (3-4 messages)
3. Booking detection with card display
4. Mobile responsive view
5. Copy functionality working
6. Error handling example

Use tools like:
- OBS Studio (free screen recording)
- Loom (browser-based)
- Browser's built-in screen recording

---

**Note**: This guide ensures the frontend is production-ready and portfolio-worthy.
