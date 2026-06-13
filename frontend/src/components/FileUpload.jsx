import { useState, useRef } from 'react';
import Spinner from './Spinner';

const FileUpload = ({ onUpload, uploading }) => {
  const [file, setFile] = useState(null);
  const [strategy, setStrategy] = useState('sentence');
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (selectedFile) => {
    const validTypes = ['application/pdf', 'text/plain'];
    if (!validTypes.includes(selectedFile.type)) {
      alert('Please upload only PDF or TXT files');
      return;
    }
    setFile(selectedFile);
  };

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleUploadClick = () => {
    if (file) {
      onUpload(file, strategy);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      <div
        className={`relative border-2 border-dashed rounded-2xl p-12 text-center transition-all ${
          dragActive
            ? 'border-primary bg-primary/10'
            : 'border-white/20 hover:border-white/40'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".pdf,.txt"
          onChange={handleInputChange}
          disabled={uploading}
        />

        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center">
            <svg
              className="w-8 h-8 text-primary"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          {file ? (
            <div className="space-y-2">
              <p className="text-lg font-medium text-white">{file.name}</p>
              <p className="text-sm text-gray-400">{formatFileSize(file.size)}</p>
              <button
                onClick={() => setFile(null)}
                className="text-sm text-primary hover:text-primary/80"
              >
                Remove
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-lg font-medium text-white">
                Drag & drop your document here
              </p>
              <p className="text-sm text-gray-400">or</p>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="px-4 py-2 bg-primary hover:bg-primary/90 rounded-lg font-medium transition-colors"
              >
                Browse Files
              </button>
              <p className="text-xs text-gray-500 mt-2">
                Supports PDF and TXT files
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="space-y-3">
        <label className="block text-sm font-medium text-gray-300">
          Chunking Strategy
        </label>
        <div className="flex gap-3">
          <button
            onClick={() => setStrategy('fixed')}
            disabled={uploading}
            className={`flex-1 px-4 py-3 rounded-xl font-medium transition-all ${
              strategy === 'fixed'
                ? 'bg-primary text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            Fixed Size
          </button>
          <button
            onClick={() => setStrategy('sentence')}
            disabled={uploading}
            className={`flex-1 px-4 py-3 rounded-xl font-medium transition-all ${
              strategy === 'sentence'
                ? 'bg-primary text-white'
                : 'bg-white/5 text-gray-400 hover:bg-white/10'
            }`}
          >
            Sentence Based
          </button>
        </div>
        <p className="text-xs text-gray-500">
          {strategy === 'fixed'
            ? 'Splits text into fixed 500-character chunks'
            : 'Splits text on sentence boundaries for better context'}
        </p>
      </div>

      <button
        onClick={handleUploadClick}
        disabled={!file || uploading}
        className={`w-full py-3 rounded-xl font-medium transition-all flex items-center justify-center gap-2 ${
          !file || uploading
            ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
            : 'bg-primary hover:bg-primary/90 hover:scale-[1.02] active:scale-[0.98] text-white shadow-lg shadow-primary/20 hover:shadow-primary/40'
        }`}
      >
        {uploading ? (
          <>
            <Spinner size="sm" />
            <span>Uploading...</span>
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
              />
            </svg>
            <span>Upload Document</span>
          </>
        )}
      </button>
    </div>
  );
};

export default FileUpload;
