import { Link } from 'react-router-dom';

const Navbar = ({ documentName, showUploadButton }) => {
  return (
    <nav className="border-b border-white/10 backdrop-blur-lg bg-black/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                RAG Chat
              </h1>
              <p className="text-xs text-gray-400">Powered by AI</p>
            </div>
          </Link>

          <div className="flex items-center gap-4">
            {documentName && (
              <div className="hidden sm:flex items-center gap-2 text-sm">
                <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-gray-300">{documentName}</span>
              </div>
            )}
            {showUploadButton && (
              <Link
                to="/"
                className="px-4 py-2 bg-primary/20 hover:bg-primary/30 border border-primary/50 rounded-lg text-sm font-medium transition-colors"
              >
                Upload New
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
