import { useEffect, useRef } from 'react';
import ChatBubble from './ChatBubble';
import BookingCard from './BookingCard';
import TypingIndicator from './TypingIndicator';

const ChatWindow = ({ messages, loading }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {messages.length === 0 && !loading && (
        <div className="h-full flex items-center justify-center">
          <div className="text-center space-y-4">
            <div className="w-16 h-16 mx-auto rounded-full bg-primary/20 flex items-center justify-center">
              <svg className="w-8 h-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold text-white">Start a conversation</h3>
              <p className="text-sm text-gray-400">
                Ask questions about your uploaded document
              </p>
            </div>
            <div className="flex flex-wrap gap-2 justify-center mt-6">
              <button className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm transition-colors">
                What is this document about?
              </button>
              <button className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm transition-colors">
                Summarize the main points
              </button>
              <button className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm transition-colors">
                Schedule an interview
              </button>
            </div>
          </div>
        </div>
      )}

      {messages.map((msg, index) => (
        <div key={index}>
          <ChatBubble message={msg.content} isUser={msg.role === 'user'} />
          {msg.booking && <BookingCard booking={msg.booking} />}
        </div>
      ))}

      {loading && (
        <div className="flex justify-start">
          <div className="flex gap-3 items-center">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </div>
            <div className="px-4 py-3 bg-white/10 rounded-2xl rounded-tl-none">
              <TypingIndicator />
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;
