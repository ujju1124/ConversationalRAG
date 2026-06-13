import { useState } from 'react';
import { useApp } from '../context/AppContext';
import { copyToClipboard } from '../utils/helpers';

const Sidebar = ({ sessionId, documentId, onNewSession }) => {
  const [isOpen, setIsOpen] = useState(true);
  const { showToast } = useApp();

  const handleCopy = async (text, label) => {
    const success = await copyToClipboard(text);
    if (success) {
      showToast(`${label} copied!`, 'success');
    } else {
      showToast('Failed to copy', 'error');
    }
  };

  const InfoItem = ({ label, value, icon }) => (
    <div className="p-3 bg-white/5 rounded-lg space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={icon} />
          </svg>
          <span className="text-xs text-gray-400">{label}</span>
        </div>
        <button
          onClick={() => handleCopy(value, label)}
          className="text-xs text-primary hover:text-primary/80 transition-colors"
        >
          Copy
        </button>
      </div>
      <p className="text-xs font-mono text-white break-all">{value}</p>
    </div>
  );

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-20 left-4 z-50 w-10 h-10 bg-primary rounded-lg flex items-center justify-center"
      >
        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
        </svg>
      </button>

      <aside
        className={`fixed lg:static inset-y-0 left-0 z-40 w-80 bg-black/40 backdrop-blur-xl border-r border-white/10 p-6 space-y-6 transition-transform lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Session Info</h2>
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden w-8 h-8 rounded-lg hover:bg-white/10 flex items-center justify-center"
          >
            <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-4">
          <InfoItem
            label="Session ID"
            value={sessionId}
            icon="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
          <InfoItem
            label="Document ID"
            value={documentId}
            icon="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </div>

        <button
          onClick={onNewSession}
          className="w-full px-4 py-3 bg-primary/20 hover:bg-primary/30 border border-primary/50 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span>New Session</span>
        </button>

        <div className="pt-6 border-t border-white/10">
          <div className="space-y-2 text-xs text-gray-400">
            <p className="flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              Connected to backend
            </p>
            <p>Chat history persists in memory</p>
          </div>
        </div>
      </aside>

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
