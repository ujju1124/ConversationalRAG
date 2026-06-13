import { useState } from 'react';
import { sendMessage } from '../services/api';
import { useAppContext } from '../context/AppContext';

export const useChat = (sessionId, documentId) => {
  const [loading, setLoading] = useState(false);
  const { showToast } = useAppContext();

  const send = async (message, onSuccess) => {
    if (!message.trim() || !documentId) return;

    setLoading(true);

    try {
      const result = await sendMessage(sessionId, message, documentId);
      
      if (onSuccess) {
        onSuccess(result);
      }
      
      return result;
    } catch (error) {
      showToast(error.message, 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    send,
  };
};
