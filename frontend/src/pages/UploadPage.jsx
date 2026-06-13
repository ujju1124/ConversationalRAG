import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { useUpload } from '../hooks/useUpload';
import Navbar from '../components/Navbar';
import FileUpload from '../components/FileUpload';

const UploadPage = () => {
  const navigate = useNavigate();
  const { currentDocument, setCurrentDocument, setMessages } = useAppContext();
  const { uploading, uploadedDoc, upload } = useUpload();

  const handleUpload = async (file, strategy) => {
    try {
      const result = await upload(file, strategy);
      setCurrentDocument(result);
      // Clear old messages when uploading a new document
      setMessages([]);
    } catch (error) {
      // Error already shown by useUpload hook
    }
  };

  const handleStartChat = () => {
    if (uploadedDoc) {
      // Ensure currentDocument is set before navigating
      setCurrentDocument(uploadedDoc);
      navigate('/chat');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen dot-pattern">
      <Navbar />
      
      <div className="max-w-2xl mx-auto px-4 py-12">
        {/* Show "Back to Chat" banner if user has an active document */}
        {currentDocument && !uploadedDoc && (
          <div className="mb-6 p-4 glass-card border border-primary/30 rounded-xl flex items-center justify-between animate-fade-in">
            <div className="flex items-center gap-3">
              <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <div>
                <p className="text-sm font-medium text-white">Active Session</p>
                <p className="text-xs text-gray-400">{currentDocument.filename}</p>
              </div>
            </div>
            <button
              onClick={() => navigate('/chat')}
              className="px-4 py-2 bg-primary hover:bg-primary/90 rounded-lg text-sm font-medium transition-colors"
            >
              Back to Chat
            </button>
          </div>
        )}

        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
            Upload Your Document
          </h1>
          <p className="text-gray-400">
            Start by uploading a PDF or TXT file to chat with your documents
          </p>
        </div>

        <div className="glass-card p-8 space-y-6">
          {!uploadedDoc ? (
            <FileUpload onUpload={handleUpload} uploading={uploading} />
          ) : (
            <div className="space-y-6 animate-fade-in">
              <div className="flex items-center gap-3 p-4 bg-green-500/20 border border-green-500/50 rounded-xl">
                <svg
                  className="w-6 h-6 text-green-400 flex-shrink-0"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <div className="flex-1">
                  <p className="text-green-400 font-medium">Upload Successful!</p>
                  <p className="text-sm text-green-300/70">{uploadedDoc.filename}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="p-4 bg-white/5 rounded-lg space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Document ID</span>
                    <button
                      onClick={() => copyToClipboard(uploadedDoc.document_id)}
                      className="text-xs text-primary hover:text-primary/80"
                    >
                      Copy
                    </button>
                  </div>
                  <p className="text-sm font-mono text-white break-all">
                    {uploadedDoc.document_id}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-white/5 rounded-lg">
                    <p className="text-sm text-gray-400 mb-1">Chunks</p>
                    <p className="text-2xl font-bold text-white">
                      {uploadedDoc.chunk_count}
                    </p>
                  </div>
                  <div className="p-4 bg-white/5 rounded-lg">
                    <p className="text-sm text-gray-400 mb-1">Strategy</p>
                    <p className="text-sm font-medium text-primary capitalize">
                      {uploadedDoc.strategy}
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={handleStartChat}
                className="w-full py-3 bg-primary hover:bg-primary/90 rounded-xl font-medium transition-all flex items-center justify-center gap-2"
              >
                <span>Start Chatting</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  />
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
