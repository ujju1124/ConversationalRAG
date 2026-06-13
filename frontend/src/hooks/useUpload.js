import { useState } from 'react';
import { ingestDocument } from '../services/api';
import { useAppContext } from '../context/AppContext';

export const useUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadedDoc, setUploadedDoc] = useState(null);
  const { showToast } = useAppContext();

  const upload = async (file, strategy) => {
    setUploading(true);
    setUploadedDoc(null);

    try {
      const result = await ingestDocument(file, strategy);
      setUploadedDoc(result);
      showToast('Document uploaded successfully!', 'success');
      return result;
    } catch (error) {
      showToast(error.message, 'error');
      throw error;
    } finally {
      setUploading(false);
    }
  };

  const reset = () => {
    setUploadedDoc(null);
  };

  return {
    uploading,
    uploadedDoc,
    upload,
    reset,
  };
};
