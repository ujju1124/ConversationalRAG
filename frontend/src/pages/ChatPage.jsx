import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { useChat } from '../hooks/useChat';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';

const ChatPage = () => {
  const navigate = useNavigate();
  const {
    currentDocument,
    currentSession,
    messages,
    addMessage,
    resetSession,
  } = useAppContext();

  const [input, setInput] = useState('');
  const { loading, send } = useChat(currentSession, currentDocument?.document_id);
  const [sessionListKey, setSessionListKey] = useState(0); // Force sidebar refresh

  useEffect(() => {
    if (!currentDocument) {
      navigate('/');
    }
  }, [currentDocument, navigate]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');

    addMessage({ role: 'user', content: userMessage });

    try {
      const result = await send(userMessage);
      addMessage({
        role: 'assistant',
        content: result.response,
        booking: result.booking,
      });
      
      // Trigger sidebar refresh by updating key
      setSessionListKey(prev => prev + 1);
    } catch (error) {
      // Error already shown by useChat hook
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!currentDocument) {
    return null;
  }

  return (
    <div className="h-screen flex flex-col dot-pattern">
      <Navbar
        documentName={currentDocument.filename}
        showUploadButton={true}
      />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar key={sessionListKey} />

        <div className="flex-1 flex flex-col">
          <ChatWindow messages={messages} loading={loading} />

          <div className="border-t border-white/10 bg-black/20 backdrop-blur-xl p-4">
            <div className="max-w-4xl mx-auto">
              <div className="flex gap-3 items-end">
                <div className="flex-1 relative">
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question about your document..."
                    disabled={loading}
                    rows={1}
                    className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-primary resize-none max-h-32"
                    style={{
                      minHeight: '48px',
                      height: 'auto',
                    }}
                    onInput={(e) => {
                      e.target.style.height = 'auto';
                      e.target.style.height = e.target.scrollHeight + 'px';
                    }}
                  />
                  <div className="absolute bottom-2 right-2 text-xs text-gray-500">
                    {input.length} / 1000
                  </div>
                </div>

                <button
                  onClick={handleSend}
                  disabled={!input.trim() || loading}
                  className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all ${
                    !input.trim() || loading
                      ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                      : 'bg-primary hover:bg-primary/90 text-white'
                  }`}
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                    />
                  </svg>
                </button>
              </div>

              <p className="text-xs text-gray-500 mt-2 text-center">
                Press Enter to send, Shift+Enter for new line
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
