import { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, MessageSquare, BookOpen, History,
  Shield, ChevronLeft, ChevronRight, Sprout, Wheat, X
} from 'lucide-react';
import Logo from './Logo';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, exact: true },
  { to: '/chat', label: 'AI Chatbot', icon: MessageSquare },
  { to: '/crops', label: 'Crop Diseases', icon: BookOpen },
  { to: '/history', label: 'Chat History', icon: History },
  { to: '/admin', label: 'Admin Panel', icon: Shield },
];

export default function Sidebar({ isOpen, onClose }) {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  // Close mobile sidebar on route change
  useEffect(() => {
    if (onClose) onClose();
  }, [location.pathname, onClose]);

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 h-full bg-primary-900 text-white z-30 flex flex-col
          transition-all duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          ${collapsed ? 'w-16' : 'w-64'}
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-primary-700">
          {!collapsed && <Logo size="sm" />}
          {collapsed && (
            <div className="mx-auto bg-primary-700 p-1.5 rounded-lg">
              <Sprout size={20} className="text-white" />
            </div>
          )}

          {/* Mobile close */}
          <button
            onClick={onClose}
            className="lg:hidden text-primary-300 hover:text-white transition-colors"
          >
            <X size={20} />
          </button>

          {/* Desktop collapse toggle */}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="hidden lg:flex items-center justify-center w-7 h-7 rounded-full
                       bg-primary-700 hover:bg-primary-600 text-primary-200 hover:text-white
                       transition-all duration-200"
          >
            {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 overflow-y-auto">
          <div className="space-y-1 px-2">
            {navItems.map(({ to, label, icon: Icon, exact }) => (
              <NavLink
                key={to}
                to={to}
                end={exact}
                className={({ isActive }) => `
                  flex items-center gap-3 px-3 py-2.5 rounded-lg font-medium text-sm
                  transition-all duration-200 group
                  ${isActive
                    ? 'bg-primary-600 text-white shadow-md'
                    : 'text-primary-200 hover:bg-primary-800 hover:text-white'
                  }
                  ${collapsed ? 'justify-center' : ''}
                `}
              >
                <Icon size={18} className="shrink-0" />
                {!collapsed && <span>{label}</span>}
                {collapsed && (
                  <span className="absolute left-16 bg-primary-800 text-white text-xs px-2 py-1
                                   rounded-md opacity-0 group-hover:opacity-100 pointer-events-none
                                   whitespace-nowrap z-50 transition-opacity">
                    {label}
                  </span>
                )}
              </NavLink>
            ))}
          </div>
        </nav>

        {/* Footer */}
        {!collapsed && (
          <div className="p-4 border-t border-primary-700">
            <div className="flex items-center gap-2 text-primary-400 text-xs">
              <Wheat size={14} />
              <span>Agricultural AI Assistant</span>
            </div>
            <div className="text-primary-500 text-xs mt-1">v1.0.0 • RAG Powered</div>
          </div>
        )}
      </aside>
    </>
  );
}

