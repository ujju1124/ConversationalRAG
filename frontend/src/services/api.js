import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ingestDocument = async (file, strategy) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      `${API_BASE_URL}/ingest?strategy=${strategy}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 'Failed to upload document';
    throw new Error(errorMessage);
  }
};

export const sendMessage = async (sessionId, message, documentId) => {
  try {
    const response = await api.post('/chat', {
      session_id: sessionId,
      user_message: message,
      document_id: documentId,
    });

    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 'Failed to send message';
    throw new Error(errorMessage);
  }
};

// ==================== SESSION HISTORY API ====================

export const getSessions = async () => {
  try {
    const response = await api.get('/sessions');
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 'Failed to fetch sessions';
    throw new Error(errorMessage);
  }
};

export const getSessionMessages = async (sessionId) => {
  try {
    const response = await api.get(`/sessions/${sessionId}/messages`);
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 'Failed to fetch messages';
    throw new Error(errorMessage);
  }
};

export const deleteSession = async (sessionId) => {
  try {
    const response = await api.delete(`/sessions/${sessionId}`);
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || 'Failed to delete session';
    throw new Error(errorMessage);
  }
};

export default api;
