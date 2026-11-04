import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { useChat } from '../context/ChatContext';

const SUGGESTED = [
  'What are rice blast symptoms?',
  'How to prevent tomato late blight?',
  'Wheat rust management methods?',
  'Causes of cotton leaf curl virus?',
];

export default function ChatInput() {
  const { sendMessage, isLoading } = useChat();
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = 'auto';
      ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
    }
  }, [input]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-gray-100 bg-white p-4">
      {/* Suggestions */}
      <div className="flex gap-2 mb-3 overflow-x-auto pb-1 scrollbar-hide">
        {SUGGESTED.map((s) => (
          <button
            key={s}
            onClick={() => { setInput(s); textareaRef.current?.focus(); }}
            disabled={isLoading}
            className="whitespace-nowrap text-xs bg-primary-50 text-primary-700 border border-primary-200 
                       rounded-full px-3 py-1.5 hover:bg-primary-100 transition-colors shrink-0
                       disabled:opacity-50"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Input row */}
      <form onSubmit={handleSubmit} className="flex items-end gap-2">
        <div className="flex-1 bg-gray-50 border border-gray-200 rounded-2xl flex items-end 
                        focus-within:border-primary-400 focus-within:ring-2 focus-within:ring-primary-100
                        transition-all duration-200 px-4 py-2">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about crop diseases, symptoms, prevention..."
            disabled={isLoading}
            rows={1}
            className="flex-1 bg-transparent resize-none text-sm text-gray-800 placeholder-gray-400 
                       focus:outline-none max-h-40 leading-relaxed py-1"
          />
        </div>

        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className="w-10 h-10 rounded-xl bg-primary-700 hover:bg-primary-800 
                     disabled:bg-gray-200 disabled:cursor-not-allowed
                     flex items-center justify-center transition-all duration-200 shadow-sm
                     hover:shadow-md active:scale-95 shrink-0"
        >
          <Send size={16} className={input.trim() && !isLoading ? 'text-white' : 'text-gray-400'} />
        </button>
      </form>

      <p className="text-center text-xs text-gray-400 mt-2">
        Powered by RAG • Answers grounded in agricultural knowledge base
      </p>
    </div>
  );
}

