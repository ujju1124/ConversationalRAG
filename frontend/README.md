# RAG Chat Frontend

Modern, dark-themed React frontend for the Conversational RAG Backend.

## Features

- 🎨 Modern dark theme with glassmorphism effects
- 📁 Drag-and-drop document upload (PDF/TXT)
- 💬 Real-time conversational chat interface
- 🔖 Automatic booking detection with visual cards
- 📱 Fully responsive design (mobile-friendly)
- ⚡ Built with Vite for fast development
- 🎭 Smooth animations and transitions

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **React Router** - Client-side routing
- **Axios** - HTTP client

## Prerequisites

- Node.js 16+ and npm
- Backend server running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── FileUpload.jsx
│   │   ├── ChatWindow.jsx
│   │   ├── ChatBubble.jsx
│   │   ├── BookingCard.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Toast.jsx
│   │   ├── Spinner.jsx
│   │   └── TypingIndicator.jsx
│   ├── pages/           # Page components
│   │   ├── UploadPage.jsx
│   │   ├── ChatPage.jsx
│   │   └── NotFound.jsx
│   ├── services/        # API integration
│   │   └── api.js
│   ├── hooks/           # Custom React hooks
│   │   ├── useChat.js
│   │   └── useUpload.js
│   ├── context/         # Global state management
│   │   └── AppContext.jsx
│   ├── utils/           # Helper functions
│   │   └── helpers.js
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── package.json
└── vite.config.js
```

## Usage

### Upload Document

1. Navigate to the home page (`/`)
2. Drag and drop a PDF or TXT file, or click to browse
3. Select chunking strategy:
   - **Fixed Size**: Split into 500-character chunks
   - **Sentence Based**: Split by sentence boundaries
4. Click "Upload Document"
5. After successful upload, click "Start Chatting"

### Chat Interface

1. Type your message in the input box at the bottom
2. Press **Enter** to send (Shift+Enter for new line)
3. View AI responses in real-time with typing indicator
4. If booking information is detected, a green booking card appears
5. Chat history persists during the session
6. Use sidebar to view session/document IDs (click to copy)

### Booking Detection

The system automatically detects booking requests containing:
- Name
- Email
- Date
- Time

When detected, a special green booking card displays the details below the assistant's message.

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Environment Variables

The frontend expects the backend to be running at:
```
http://localhost:8000
```

To change this, update the `BASE_URL` in `src/services/api.js`

## Design System

### Colors
- Background: `#0f0f0f`
- Accent: `#6366f1` (Electric Indigo)
- Success: `#10b981` (Green for bookings)
- Error: `#ef4444` (Red for errors)

### Effects
- Glassmorphism cards with backdrop blur
- Dot grid pattern background
- Smooth fade and slide animations
- Custom scrollbar styling

## API Integration

The frontend communicates with two backend endpoints:

### POST /ingest
Upload document with chunking strategy
```javascript
{
  file: File,
  strategy: "fixed" | "sentence"
}
```

### POST /chat
Send message and get response
```javascript
{
  session_id: string,
  user_message: string,
  document_id: string
}
```

## State Management

Uses React Context API (`AppContext`) to manage:
- Current document information
- Active session ID
- Chat message history
- Toast notifications

No Redux required - simple and effective.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Troubleshooting

**Frontend won't start:**
- Ensure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again

**Can't upload documents:**
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Ensure file is PDF or TXT format

**Chat not working:**
- Verify you uploaded a document first
- Check Network tab for API errors
- Ensure `document_id` is present in state

## License

This project is part of a portfolio demonstration.

## Author

Built as a portfolio project by Ujwal
