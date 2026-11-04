import { useState, useEffect } from 'react';
import { Menu, Settings as SettingsIcon, User, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';
import Logo from './Logo';
import { adminAPI, getApiBaseUrl } from '../api';

export default function Header({ onMenuClick }) {
  const [backendStatus, setBackendStatus] = useState('checking'); // 'connected' | 'error' | 'checking'
  const [showConfig, setShowConfig] = useState(false);
  const [customUrl, setCustomUrl] = useState(getApiBaseUrl());

  const checkHealth = () => {
    setBackendStatus('checking');
    adminAPI.health()
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('error'));
  };

  useEffect(() => {
    checkHealth();
  }, []);

  const handleSaveUrl = (e) => {
    e.preventDefault();
    if (customUrl.trim()) {
      localStorage.setItem('backend_url', customUrl.trim());
      setShowConfig(false);
      checkHealth();
      window.location.reload();
    }
  };

  return (
    <>
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between sticky top-0 z-10 shadow-sm">
        {/* Left: hamburger + logo (mobile) */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuClick}
            className="lg:hidden text-gray-600 hover:text-primary-700 transition-colors p-1"
          >
            <Menu size={22} />
          </button>
          <div className="lg:hidden">
            <Logo size="sm" />
          </div>
        </div>

        {/* Center: title (desktop) */}
        <div className="hidden lg:block">
          <h1 className="text-lg font-semibold text-gray-800">Crop Disease Knowledge Assistant</h1>
        </div>

        {/* Right: status + icons */}
        <div className="flex items-center gap-3">
          {/* Backend Status indicator */}
          <button
            onClick={() => setShowConfig(true)}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-all ${
              backendStatus === 'connected'
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : backendStatus === 'checking'
                ? 'bg-amber-50 text-amber-700 border border-amber-200 animate-pulse'
                : 'bg-rose-50 text-rose-700 border border-rose-200'
            }`}
            title="Click to view or edit backend API URL"
          >
            {backendStatus === 'connected' ? (
              <>
                <CheckCircle2 size={13} className="text-emerald-600" />
                <span className="hidden sm:inline">Backend Live</span>
              </>
            ) : backendStatus === 'checking' ? (
              <>
                <RefreshCw size={13} className="animate-spin text-amber-600" />
                <span className="hidden sm:inline">Waking Up...</span>
              </>
            ) : (
              <>
                <AlertCircle size={13} className="text-rose-600" />
                <span className="hidden sm:inline">API Config</span>
              </>
            )}
            <SettingsIcon size={12} className="opacity-70 ml-0.5" />
          </button>

          <div className="flex items-center gap-2 pl-2 border-l border-gray-200">
            <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
              <User size={16} className="text-primary-700" />
            </div>
            <div className="hidden sm:block">
              <div className="text-sm font-medium text-gray-700">Farmer</div>
              <div className="text-xs text-gray-400">User</div>
            </div>
          </div>
        </div>
      </header>

      {/* Backend URL Configuration Modal */}
      {showConfig && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl animate-fade-in border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
                <SettingsIcon size={18} className="text-primary-700" /> Backend API URL
              </h3>
              <button
                onClick={() => setShowConfig(false)}
                className="text-gray-400 hover:text-gray-600 text-lg font-bold"
              >
                ✕
              </button>
            </div>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              If your backend is hosted on Render, paste its URL here (e.g. <code>https://crop-disease-knowledge.onrender.com</code>). 
              Render free tier spins down after inactivity and takes ~30-50s to wake up on the first request.
            </p>
            <form onSubmit={handleSaveUrl} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-gray-700 block mb-1">
                  API Server URL:
                </label>
                <input
                  type="url"
                  required
                  value={customUrl}
                  onChange={(e) => setCustomUrl(e.target.value)}
                  placeholder="https://your-service.onrender.com"
                  className="input-field"
                />
              </div>
              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => {
                    localStorage.removeItem('backend_url');
                    setCustomUrl(getApiBaseUrl());
                    setShowConfig(false);
                    checkHealth();
                  }}
                  className="text-xs text-gray-500 hover:text-gray-700 px-3 py-2"
                >
                  Reset Default
                </button>
                <button
                  type="submit"
                  className="btn-primary text-xs px-4 py-2"
                >
                  Save & Connect
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
