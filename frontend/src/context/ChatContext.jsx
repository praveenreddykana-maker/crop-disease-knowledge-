import React, { createContext, useContext, useState, useCallback } from 'react';
import { chatAPI } from '../api';

const ChatContext = createContext(null);

export function ChatProvider({ children }) {
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadHistory = useCallback(async () => {
    try {
      const res = await chatAPI.getHistory();
      setConversations(res.data.conversations || []);
    } catch (e) {
      console.error('Failed to load history:', e);
    }
  }, []);

  const loadConversation = useCallback(async (id) => {
    try {
      const res = await chatAPI.getConversation(id);
      setActiveConversationId(id);
      setMessages(res.data.messages || []);
    } catch (e) {
      console.error('Failed to load conversation:', e);
    }
  }, []);

  const sendMessage = useCallback(async (question) => {
    if (!question.trim() || isLoading) return;

    // Optimistically add user message
    const userMsg = { role: 'user', content: question, timestamp: new Date().toISOString() };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);

    try {
      const res = await chatAPI.sendMessage(question, activeConversationId);
      const { answer, sources, conversation_id } = res.data;

      // Set/update conversation ID
      setActiveConversationId(conversation_id);

      // Add assistant message
      const assistantMsg = {
        role: 'assistant',
        content: answer,
        sources: sources || [],
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);

      // Refresh sidebar history
      loadHistory();
    } catch (e) {
      const errMsg = e.response?.data?.detail || 'Failed to get a response. Please try again.';
      setError(errMsg);
      // Remove optimistic user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  }, [activeConversationId, isLoading, loadHistory]);

  const startNewChat = useCallback(() => {
    setActiveConversationId(null);
    setMessages([]);
    setError(null);
  }, []);

  const deleteConversation = useCallback(async (id) => {
    try {
      await chatAPI.deleteConversation(id);
      if (activeConversationId === id) startNewChat();
      loadHistory();
    } catch (e) {
      console.error('Failed to delete conversation:', e);
    }
  }, [activeConversationId, startNewChat, loadHistory]);

  const clearAllHistory = useCallback(async () => {
    try {
      await chatAPI.clearAllHistory();
      startNewChat();
      setConversations([]);
    } catch (e) {
      console.error('Failed to clear history:', e);
    }
  }, [startNewChat]);

  return (
    <ChatContext.Provider
      value={{
        conversations,
        activeConversationId,
        messages,
        isLoading,
        error,
        loadHistory,
        loadConversation,
        sendMessage,
        startNewChat,
        deleteConversation,
        clearAllHistory,
        setError,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export const useChat = () => {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error('useChat must be used within ChatProvider');
  return ctx;
};

