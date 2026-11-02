import React from 'react';
import { Menu, Bell, User } from 'lucide-react';
import Logo from './Logo';

export default function Header({ onMenuClick }) {
  return (
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

      {/* Right: icons */}
      <div className="flex items-center gap-2">
        <button className="relative p-2 rounded-lg text-gray-500 hover:text-primary-700 hover:bg-primary-50 transition-all">
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-accent-500 rounded-full"></span>
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
  );
}

