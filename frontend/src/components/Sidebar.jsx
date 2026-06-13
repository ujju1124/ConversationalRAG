import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { useSessionHistory } from '../hooks/useSessionHistory';
import { copyToClipboard } from '../utils/helpers';

const Sidebar = () => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(true);
  const { 
    currentSession, 
    currentDocument,
    showToast,
    loadSession,
    resetSession,
    setMessages
  } = useAppContext();
  
  const { sessions, loading, removeSession, fetchSessions } = useSessionHistory();

  const handleCopy = async (text, label) => {
    const success = await copyToClipboard(text);
    if (success) {
      showToast(`${label} copied!`, 'success');
    } else {
      showToast('Failed to copy', 'error');
    }
  };

  const handleNewChat = () => {
    // Generate new session ID and clear messages
    resetSession();
    // If no document loaded, navigate to upload
    if (!currentDocument) {
      navigate('/');
    }
  };

  const handleSessionClick = async (session) => {
    const success = await loadSession(
      session.session_id,
      session.document_id,
      session.document_name
    );
    
    if (success) {
      navigate('/chat');
      // Refresh sessions to update "active" status
      fetchSessions();
    }
  };

  const handleDeleteSession = async (e, sessionId) => {
    e.stopPropagation(); // Prevent session click
    
    const success = await removeSession(sessionId);
    if (success) {
      showToast('Session deleted', 'success');
      // If deleted session was current, reset
      if (sessionId === currentSession) {
        handleNewChat();
      }
    } else {
      showToast('Failed to delete session', 'error');
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <>
      {/* Mobile toggle button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-20 left-4 z-50 w-10 h-10 bg-primary rounded-lg flex items-center justify-center shadow-lg"
      >
        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
        </svg>
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-80 bg-black/40 backdrop-blur-xl border-r border-white/10 flex flex-col transition-transform lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Top Section - New Chat Button */}
        <div className="p-4 border-b border-white/10">
          <button
            onClick={handleNewChat}
            className="w-full px-4 py-3 bg-primary hover:bg-primary/90 rounded-lg font-medium transition-all flex items-center justify-center gap-2 shadow-lg shadow-primary/20"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>New Chat</span>
          </button>
        </div>

        {/* Middle Section - Chat History */}
        <div className="flex-1 overflow-y-auto p-4">
          <h2 className="text-sm font-semibold text-gray-400 mb-3 px-2">Chat History</h2>
          
          {loading ? (
            <div className="space-y-2">
              {[1, 2, 3].map(i => (
                <div key={i} className="p-3 bg-white/5 rounded-lg animate-pulse">
                  <div className="h-4 bg-white/10 rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-white/10 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : sessions.length === 0 ? (
            <div className="text-center py-8 text-gray-500 text-sm">
              <svg className="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p>No chat history yet</p>
              <p className="text-xs mt-1">Start a conversation!</p>
            </div>
          ) : (
            <div className="space-y-2">
              {sessions.map((session) => (
                <div
                  key={session.session_id}
                  onClick={() => handleSessionClick(session)}
                  className={`group relative p-3 rounded-lg cursor-pointer transition-all ${
                    session.session_id === currentSession
                      ? 'bg-primary/20 border border-primary/50'
                      : 'bg-white/5 hover:bg-white/10 border border-transparent'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white truncate">
                        {session.title || 'New Conversation'}
                      </p>
                      <p className="text-xs text-gray-400 truncate mt-1">
                        {session.document_name}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <p className="text-xs text-gray-500">
                          {formatTimestamp(session.updated_at)}
                        </p>
                        <span className="text-xs text-gray-600">•</span>
                        <p className="text-xs text-gray-500">
                          {session.message_count} msgs
                        </p>
                      </div>
                    </div>
                    
                    <button
                      onClick={(e) => handleDeleteSession(e, session.session_id)}
                      className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-500/20 rounded transition-all"
                    >
                      <svg className="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Bottom Section - Current Session Info */}
        <div className="p-4 border-t border-white/10 space-y-3">
          {currentDocument && (
            <div className="p-3 bg-white/5 rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Session ID</span>
                <button
                  onClick={() => handleCopy(currentSession, 'Session ID')}
                  className="text-xs text-primary hover:text-primary/80 transition-colors"
                >
                  Copy
                </button>
              </div>
              <p className="text-xs font-mono text-white break-all">{currentSession}</p>
            </div>
          )}

          {currentDocument && (
            <div className="p-3 bg-white/5 rounded-lg space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">Document ID</span>
                <button
                  onClick={() => handleCopy(currentDocument.document_id, 'Document ID')}
                  className="text-xs text-primary hover:text-primary/80 transition-colors"
                >
                  Copy
                </button>
              </div>
              <p className="text-xs font-mono text-white break-all">{currentDocument.document_id}</p>
            </div>
          )}

          <div className="pt-2 text-xs text-gray-400 flex items-center gap-2">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            Connected to backend
          </div>
        </div>
      </aside>

      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
};

export default Sidebar;
