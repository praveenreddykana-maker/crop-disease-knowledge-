import React, { useEffect, useState } from 'react';
import {
  History, Search, Trash2, MessageSquare, AlertCircle, X, RefreshCw
} from 'lucide-react';
import { useChat } from '../context/ChatContext';
import { useNavigate } from 'react-router-dom';

function ConvItem({ conv, onOpen, onDelete }) {
  return (
    <div className="card flex items-start gap-3 hover:border-primary-200 transition-all group">
      <div className="w-9 h-9 rounded-full bg-primary-100 flex items-center justify-center shrink-0 mt-0.5">
        <MessageSquare size={16} className="text-primary-700" />
      </div>
      <div className="flex-1 min-w-0">
        <button
          onClick={() => onOpen(conv.id)}
          className="text-left w-full"
        >
          <div className="font-semibold text-gray-800 text-sm truncate group-hover:text-primary-700">
            {conv.title || 'Untitled conversation'}
          </div>
          {conv.last_message && (
            <div className="text-xs text-gray-400 mt-0.5 truncate">{conv.last_message}</div>
          )}
          <div className="flex items-center gap-3 mt-1">
            <span className="text-xs text-gray-400">
              {conv.message_count} message{conv.message_count !== 1 ? 's' : ''}
            </span>
            <span className="text-xs text-gray-300">•</span>
            <span className="text-xs text-gray-400">
              {conv.updated_at
                ? new Date(conv.updated_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
                : ''}
            </span>
          </div>
        </button>
      </div>
      <button
        onClick={() => onDelete(conv.id)}
        className="text-gray-300 hover:text-red-500 transition-colors p-1 shrink-0"
        title="Delete conversation"
      >
        <Trash2 size={14} />
      </button>
    </div>
  );
}

export default function HistoryPage() {
  const { conversations, loadHistory, loadConversation, deleteConversation, clearAllHistory } = useChat();
  const [searchQuery, setSearchQuery] = useState('');
  const [confirmClear, setConfirmClear] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const handleOpen = async (id) => {
    await loadConversation(id);
    navigate('/chat');
  };

  const filtered = conversations.filter((c) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return c.title?.toLowerCase().includes(q) || c.last_message?.toLowerCase().includes(q);
  });

  return (
    <div className="p-6 max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <History size={22} className="text-primary-700" /> Chat History
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            {conversations.length} conversation{conversations.length !== 1 ? 's' : ''} stored
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadHistory}
            className="btn-secondary text-sm flex items-center gap-1.5"
          >
            <RefreshCw size={14} /> Refresh
          </button>
          {conversations.length > 0 && (
            <button
              onClick={() => setConfirmClear(true)}
              className="text-sm flex items-center gap-1.5 px-3 py-2 rounded-lg border border-red-200 
                         text-red-600 hover:bg-red-50 transition-all"
            >
              <Trash2 size={14} /> Clear All
            </button>
          )}
        </div>
      </div>

      {/* Clear confirmation */}
      {confirmClear && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-xl p-4 flex items-center justify-between">
          <span className="text-sm text-red-700 font-medium">
            Delete all {conversations.length} conversations permanently?
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => { clearAllHistory(); setConfirmClear(false); }}
              className="text-sm px-3 py-1.5 rounded-lg bg-red-600 text-white hover:bg-red-700"
            >
              Yes, clear all
            </button>
            <button
              onClick={() => setConfirmClear(false)}
              className="text-sm px-3 py-1.5 rounded-lg border border-gray-200 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="relative mb-4">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search conversations..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="input-field pl-9"
        />
        {searchQuery && (
          <button onClick={() => setSearchQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
            <X size={14} />
          </button>
        )}
      </div>

      {/* List */}
      {filtered.length === 0 ? (
        <div className="text-center py-16">
          <History size={40} className="text-gray-200 mx-auto mb-3" />
          <p className="text-gray-400 font-medium">
            {searchQuery ? 'No conversations match your search.' : 'No conversations yet.'}
          </p>
          {!searchQuery && (
            <p className="text-gray-400 text-sm mt-1">
              Start chatting to see your history here.
            </p>
          )}
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((conv) => (
            <ConvItem
              key={conv.id}
              conv={conv}
              onOpen={handleOpen}
              onDelete={deleteConversation}
            />
          ))}
        </div>
      )}
    </div>
  );
}
