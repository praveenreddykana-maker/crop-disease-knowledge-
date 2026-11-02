import React, { useState, useEffect } from 'react';
import {
  Shield, Lock, Upload, FileText, Trash2, CheckCircle,
  XCircle, Clock, Database, RefreshCw, AlertTriangle, X
} from 'lucide-react';
import { adminAPI, documentsAPI } from '../api';

function StatusBadge({ status }) {
  const map = {
    indexed: { cls: 'bg-green-100 text-green-700', icon: <CheckCircle size={12} />, label: 'Indexed' },
    processing: { cls: 'bg-yellow-100 text-yellow-700', icon: <Clock size={12} />, label: 'Processing' },
    error: { cls: 'bg-red-100 text-red-700', icon: <XCircle size={12} />, label: 'Error' },
  };
  const s = map[status] || map.processing;
  return (
    <span className={`flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full ${s.cls}`}>
      {s.icon} {s.label}
    </span>
  );
}

function LoginForm({ onLogin }) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await adminAPI.login(password);
      if (res.data.success) {
        localStorage.setItem('adminToken', res.data.token);
        onLogin(res.data.token);
      }
    } catch {
      setError('Invalid admin password. Check your .env file (ADMIN_PASSWORD).');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[60vh] flex items-center justify-center p-6">
      <div className="card max-w-sm w-full shadow-lg">
        <div className="text-center mb-6">
          <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center mx-auto mb-3">
            <Shield size={28} className="text-primary-700" />
          </div>
          <h2 className="text-xl font-bold text-gray-800">Admin Panel</h2>
          <p className="text-gray-500 text-sm mt-1">Enter admin password to continue</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="password"
              placeholder="Admin password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field pl-9"
              required
            />
          </div>
          {error && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
              {error}
            </div>
          )}
          <button type="submit" disabled={loading} className="btn-primary w-full justify-center">
            {loading ? 'Authenticating...' : 'Login'}
          </button>
        </form>
        <p className="text-xs text-gray-400 text-center mt-4">
          Default password: <code className="bg-gray-100 px-1 rounded">admin123</code>
        </p>
      </div>
    </div>
  );
}

export default function AdminPage() {
  const [token, setToken] = useState(localStorage.getItem('adminToken') || '');
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const loadData = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const [docsRes, statsRes] = await Promise.all([
        documentsAPI.getDocuments(token),
        documentsAPI.getStats(token),
      ]);
      setDocuments(docsRes.data.documents || []);
      setStats(statsRes.data);
    } catch (e) {
      if (e.response?.status === 403) {
        localStorage.removeItem('adminToken');
        setToken('');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [token]);

  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    setUploadMsg(null);
    try {
      const res = await documentsAPI.uploadDocument(file, token);
      setUploadMsg({ type: 'success', text: res.data.message });
      loadData();
    } catch (e) {
      setUploadMsg({ type: 'error', text: e.response?.data?.detail || 'Upload failed.' });
    } finally {
      setUploading(false);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleUpload(file);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this document from the knowledge base?')) return;
    try {
      await documentsAPI.deleteDocument(id, token);
      loadData();
    } catch (e) {
      alert('Failed to delete document.');
    }
  };

  if (!token) return <LoginForm onLogin={setToken} />;

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Shield size={22} className="text-primary-700" /> Admin Panel
          </h1>
          <p className="text-sm text-gray-500 mt-1">Manage the agricultural knowledge base</p>
        </div>
        <div className="flex gap-2">
          <button onClick={loadData} className="btn-secondary text-sm flex items-center gap-1.5">
            <RefreshCw size={14} /> Refresh
          </button>
          <button
            onClick={() => { localStorage.removeItem('adminToken'); setToken(''); }}
            className="text-sm px-3 py-2 rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Total Documents', value: stats.total_documents, icon: <FileText size={18} className="text-blue-600" />, cls: 'bg-blue-50' },
            { label: 'Indexed', value: stats.indexed_documents, icon: <CheckCircle size={18} className="text-green-600" />, cls: 'bg-green-50' },
            { label: 'Failed', value: stats.failed_documents, icon: <XCircle size={18} className="text-red-600" />, cls: 'bg-red-50' },
            { label: 'Vector Chunks', value: stats.vector_store_size, icon: <Database size={18} className="text-purple-600" />, cls: 'bg-purple-50' },
          ].map(({ label, value, icon, cls }) => (
            <div key={label} className={`card ${cls} border-0`}>
              <div className="flex items-center gap-3">
                {icon}
                <div>
                  <div className="text-xl font-bold text-gray-800">{value}</div>
                  <div className="text-xs text-gray-500">{label}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload */}
      <div className="card">
        <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Upload size={18} className="text-primary-700" /> Upload Document
        </h2>

        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-all
            ${dragOver ? 'border-primary-500 bg-primary-50' : 'border-gray-200 hover:border-primary-300'}`}
        >
          <Upload size={32} className="mx-auto text-gray-300 mb-3" />
          <p className="text-gray-600 font-medium text-sm mb-1">
            Drag & drop a PDF here, or click to browse
          </p>
          <p className="text-xs text-gray-400 mb-4">PDF files only • Max 50MB</p>
          <label className="btn-primary cursor-pointer inline-flex items-center gap-2 text-sm">
            <Upload size={14} />
            {uploading ? 'Uploading...' : 'Choose PDF File'}
            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={handleFileInput}
              disabled={uploading}
            />
          </label>
        </div>

        {uploadMsg && (
          <div className={`mt-3 p-3 rounded-lg flex items-start gap-2 text-sm
            ${uploadMsg.type === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}`}>
            {uploadMsg.type === 'success' ? <CheckCircle size={16} /> : <AlertTriangle size={16} />}
            <span className="flex-1">{uploadMsg.text}</span>
            <button onClick={() => setUploadMsg(null)}><X size={14} /></button>
          </div>
        )}
      </div>

      {/* Documents list */}
      <div className="card">
        <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Database size={18} className="text-primary-700" />
          Uploaded Documents
          <span className="ml-auto text-xs text-gray-400 font-normal">
            {documents.length} document{documents.length !== 1 ? 's' : ''}
          </span>
        </h2>

        {loading ? (
          <div className="text-center py-8 text-gray-400 text-sm">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="text-center py-8">
            <FileText size={32} className="text-gray-200 mx-auto mb-2" />
            <p className="text-gray-400 text-sm">No documents uploaded yet.</p>
            <p className="text-gray-400 text-xs mt-1">
              The system uses the built-in agricultural knowledge base by default.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {documents.map((doc) => (
              <div key={doc.id}
                className="flex items-center gap-3 p-3 rounded-xl bg-gray-50 border border-gray-100">
                <FileText size={20} className="text-primary-600 shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm text-gray-800 truncate">{doc.original_name}</div>
                  <div className="flex items-center gap-3 mt-0.5">
                    <span className="text-xs text-gray-400">
                      {(doc.file_size / 1024).toFixed(0)} KB
                    </span>
                    {doc.chunk_count > 0 && (
                      <span className="text-xs text-gray-400">{doc.chunk_count} chunks</span>
                    )}
                    <span className="text-xs text-gray-400">
                      {doc.upload_time ? new Date(doc.upload_time).toLocaleDateString() : ''}
                    </span>
                  </div>
                  {doc.error_message && (
                    <div className="text-xs text-red-500 mt-0.5 truncate">{doc.error_message}</div>
                  )}
                </div>
                <StatusBadge status={doc.status} />
                <button
                  onClick={() => handleDelete(doc.id)}
                  className="text-gray-300 hover:text-red-500 transition-colors p-1.5 rounded-lg hover:bg-red-50"
                  title="Delete document"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Info */}
      <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 text-sm text-blue-800">
        <strong>ℹ️ Built-in Knowledge Base:</strong> The system includes comprehensive disease 
        profiles for Rice, Wheat, Tomato, Potato, Cotton, Maize, and Groundnut — pre-loaded at 
        startup. Upload additional PDFs above to expand the knowledge base with your own research 
        papers and agricultural guides.
      </div>
    </div>
  );
}

