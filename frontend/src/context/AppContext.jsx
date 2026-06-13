import { createContext, useState, useContext } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
};

// Alias for convenience
export const useApp = useAppContext;

export const AppProvider = ({ children }) => {
  const [currentDocument, setCurrentDocument] = useState(null);
  const [currentSession, setCurrentSession] = useState(() => {
    return crypto.randomUUID();
  });
  const [messages, setMessages] = useState([]);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'info') => {
    setToast({ message, type, id: Date.now() });
  };

  const hideToast = () => {
    setToast(null);
  };

  const resetSession = () => {
    setCurrentSession(crypto.randomUUID());
    setMessages([]); // Clear chat messages for new session
  };

  const addMessage = (message) => {
    setMessages(prev => [...prev, message]);
  };

  const value = {
    currentDocument,
    setCurrentDocument,
    currentSession,
    setCurrentSession,
    messages,
    setMessages,
    resetSession,
    addMessage,
    toast,
    showToast,
    hideToast,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
