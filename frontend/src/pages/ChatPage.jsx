import { useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { AlertCircle, X } from 'lucide-react';
import ChatMessages from '../components/ChatMessages';
import ChatInput from '../components/ChatInput';
import { useChat } from '../context/ChatContext';

export default function ChatPage() {
  const { messages, isLoading, error, sendMessage, setError } = useChat();
  const [searchParams] = useSearchParams();
  const sentRef = useRef(false);

  // Auto-send question from URL param (e.g., from dashboard suggestions)
  useEffect(() => {
    const q = searchParams.get('q');
    if (q && !sentRef.current && messages.length === 0) {
      sentRef.current = true;
      sendMessage(q);
    }
  }, [searchParams, messages.length, sendMessage]);

  return (
    <div className="flex flex-col h-full">
      {/* Page header */}
      <div className="px-4 py-3 border-b border-gray-100 bg-white">
        <h2 className="font-bold text-gray-800 text-lg">AI Agricultural Chatbot</h2>
        <p className="text-xs text-gray-500">RAG-powered • Answers from trusted agricultural sources</p>
      </div>

      {/* Error banner */}
      {error && (
        <div className="mx-4 mt-3 bg-red-50 border border-red-200 rounded-xl p-3 flex items-start gap-2">
          <AlertCircle size={16} className="text-red-500 mt-0.5 shrink-0" />
          <span className="text-sm text-red-700 flex-1">{error}</span>
          <button onClick={() => setError(null)} className="text-red-400 hover:text-red-600">
            <X size={14} />
          </button>
        </div>
      )}

      {/* Chat messages */}
      <ChatMessages messages={messages} isLoading={isLoading} />

      {/* Input */}
      <ChatInput />
    </div>
  );
}

