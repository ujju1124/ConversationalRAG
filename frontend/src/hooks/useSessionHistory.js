import { useState, useEffect } from 'react';
import { getSessions, deleteSession } from '../services/api';

export const useSessionHistory = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSessions = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getSessions();
      setSessions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const removeSession = async (sessionId) => {
    try {
      await deleteSession(sessionId);
      // Remove from local state
      setSessions(prev => prev.filter(s => s.session_id !== sessionId));
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  };

  // Auto-fetch on mount
  useEffect(() => {
    fetchSessions();
  }, []);

  return {
    sessions,
    loading,
    error,
    fetchSessions,
    removeSession,
  };
};
