import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Home, ClipboardList, Calendar, Clock, LogOut } from 'lucide-react';
import { logout } from '../services/auth';

const Layout: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
      logout();
      navigate('/');
  };

  return (
    <div className="flex h-screen bg-[#09090b] text-zinc-100">
      {/* Sidebar */}
      <aside className="w-64 bg-zinc-950/80 border-r border-zinc-800 hidden md:flex flex-col backdrop-blur-md">
        <div className="p-6 border-b border-zinc-800">
          <h1 className="text-2xl font-bold text-zinc-100 tracking-tight">Modéa</h1>
          <p className="text-sm text-zinc-500 mt-1">Panel Ucznia</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <a
            onClick={() => navigate('/dashboard')}
            className="flex items-center space-x-3 text-zinc-400 p-3 rounded-lg hover:bg-zinc-900 cursor-pointer hover:text-zinc-100 transition duration-200"
          >
            <Home size={20} />
            <span>Pulpit</span>
          </a>
          <a
            onClick={() => navigate('/dashboard/grades')}
            className="flex items-center space-x-3 text-zinc-400 p-3 rounded-lg hover:bg-zinc-900 cursor-pointer hover:text-zinc-100 transition duration-200"
          >
            <ClipboardList size={20} />
            <span>Oceny</span>
          </a>
          <a
            onClick={() => navigate('/dashboard/attendance')}
            className="flex items-center space-x-3 text-zinc-400 p-3 rounded-lg hover:bg-zinc-900 cursor-pointer hover:text-zinc-100 transition duration-200"
          >
            <Calendar size={20} />
            <span>Obecność</span>
          </a>
          <a
            onClick={() => navigate('/dashboard/timetable')}
            className="flex items-center space-x-3 text-zinc-400 p-3 rounded-lg hover:bg-zinc-900 cursor-pointer hover:text-zinc-100 transition duration-200"
          >
            <Clock size={20} />
            <span>Plan lekcji</span>
          </a>
        </nav>
        <div className="p-4 border-t border-zinc-800">
          <button
            onClick={handleLogout}
            className="flex items-center space-x-3 text-red-500 w-full p-3 rounded-lg hover:bg-red-950/30 hover:text-red-400 transition duration-200"
          >
            <LogOut size={20} />
            <span>Wyloguj</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="p-8 max-w-7xl mx-auto">
            <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
