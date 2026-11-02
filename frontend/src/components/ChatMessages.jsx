import React, { useRef, useEffect } from 'react';
import SimpleMarkdown from './SimpleMarkdown';
import { User, Bot, BookOpen, ChevronDown } from 'lucide-react';

function TypingIndicator() {
  return (
    <div className="flex items-end gap-2 chat-message">
      <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center shrink-0">
        <Bot size={16} className="text-primary-700" />
      </div>
      <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm">
        <div className="flex gap-1.5 items-center h-5">
          <div className="w-2 h-2 rounded-full bg-primary-400 typing-dot"></div>
          <div className="w-2 h-2 rounded-full bg-primary-400 typing-dot"></div>
          <div className="w-2 h-2 rounded-full bg-primary-400 typing-dot"></div>
        </div>
      </div>
    </div>
  );
}

function SourceCard({ sources }) {
  const [expanded, setExpanded] = React.useState(false);
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1.5 text-xs text-primary-600 hover:text-primary-800 
                   font-medium transition-colors"
      >
        <BookOpen size={12} />
        <span>{sources.length} source{sources.length > 1 ? 's' : ''}</span>
        <ChevronDown
          size={12}
          className={`transition-transform ${expanded ? 'rotate-180' : ''}`}
        />
      </button>
      {expanded && (
        <div className="mt-2 space-y-2">
          {sources.map((src, i) => (
            <div
              key={i}
              className="bg-primary-50 border border-primary-100 rounded-lg p-3 text-xs"
            >
              <div className="font-semibold text-primary-800 mb-1 flex items-center gap-1">
                <BookOpen size={11} />
                {src.source}
                {src.score != null && (
                  <span className="ml-auto text-primary-400 font-normal">
                    relevance: {(1 - src.score).toFixed(2)}
                  </span>
                )}
              </div>
              {src.content && (
                <div className="text-gray-600 line-clamp-3">{src.content}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Message({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex items-end gap-2 chat-message ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm
          ${isUser ? 'bg-accent-400' : 'bg-primary-100'}`}
      >
        {isUser
          ? <User size={16} className="text-white" />
          : <Bot size={16} className="text-primary-700" />
        }
      </div>

      {/* Bubble */}
      <div className={`max-w-[80%] md:max-w-[70%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        <div
          className={`rounded-2xl px-4 py-3 shadow-sm
            ${isUser
              ? 'bg-primary-700 text-white rounded-br-none'
              : 'bg-white border border-gray-100 text-gray-800 rounded-bl-none'
            }`}
        >
          {isUser ? (
            <p className="text-sm leading-relaxed">{message.content}</p>
          ) : (
            <div className="text-sm leading-relaxed prose-chat">
              <SimpleMarkdown>{message.content}</SimpleMarkdown>
            </div>
          )}
        </div>

        {/* Sources for assistant */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="px-1 w-full">
            <SourceCard sources={message.sources} />
          </div>
        )}

        {/* Timestamp */}
        <span className="text-xs text-gray-400 mt-1 px-1">
          {message.timestamp
            ? new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            : ''}
        </span>
      </div>
    </div>
  );
}

export default function ChatMessages({ messages, isLoading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <div className="w-20 h-20 rounded-full bg-primary-100 flex items-center justify-center mb-4">
          <Bot size={36} className="text-primary-600" />
        </div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Ask Me About Crop Diseases</h3>
        <p className="text-gray-500 text-sm max-w-md mb-6">
          I can help you identify symptoms, understand causes, and find management strategies 
          for common crop diseases using our agricultural knowledge base.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full max-w-lg">
          {[
            'What are the symptoms of rice blast disease?',
            'How can I prevent bacterial leaf blight?',
            'What causes tomato leaf curl?',
            'Management methods for wheat rust?',
          ].map((q) => (
            <div
              key={q}
              className="text-left bg-primary-50 border border-primary-100 rounded-xl p-3 
                         text-sm text-primary-700 cursor-default hover:bg-primary-100 transition-colors"
            >
              💬 {q}
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((msg, i) => (
        <Message key={i} message={msg} />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  );
}
