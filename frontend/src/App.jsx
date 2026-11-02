import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ChatProvider } from './context/ChatContext';
import Layout from './layouts/Layout';
import Dashboard from './pages/Dashboard';
import ChatPage from './pages/ChatPage';
import CropsPage from './pages/CropsPage';
import HistoryPage from './pages/HistoryPage';
import AdminPage from './pages/AdminPage';

export default function App() {
  return (
    <BrowserRouter>
      <ChatProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="chat" element={<ChatPage />} />
            <Route path="crops" element={<CropsPage />} />
            <Route path="crops/:cropName" element={<CropsPage />} />
            <Route path="history" element={<HistoryPage />} />
            <Route path="admin" element={<AdminPage />} />
          </Route>
        </Routes>
      </ChatProvider>
    </BrowserRouter>
  );
}
