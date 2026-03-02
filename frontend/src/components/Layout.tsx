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
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md hidden md:flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-600">E-Dziennik</h1>
          <p className="text-sm text-gray-500 mt-1">Student Portal</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <a
            onClick={() => navigate('/dashboard')}
            className="flex items-center space-x-3 text-gray-700 p-3 rounded-lg hover:bg-blue-50 cursor-pointer hover:text-blue-600 transition"
          >
            <Home size={20} />
            <span>Dashboard</span>
          </a>
          <a
            onClick={() => navigate('/dashboard/grades')}
            className="flex items-center space-x-3 text-gray-700 p-3 rounded-lg hover:bg-blue-50 cursor-pointer hover:text-blue-600 transition"
          >
            <ClipboardList size={20} />
            <span>Grades</span>
          </a>
          <a
            onClick={() => navigate('/dashboard/attendance')}
            className="flex items-center space-x-3 text-gray-700 p-3 rounded-lg hover:bg-blue-50 cursor-pointer hover:text-blue-600 transition"
          >
            <Calendar size={20} />
            <span>Attendance</span>
          </a>
          <a
            onClick={() => navigate('/dashboard/timetable')}
            className="flex items-center space-x-3 text-gray-700 p-3 rounded-lg hover:bg-blue-50 cursor-pointer hover:text-blue-600 transition"
          >
            <Clock size={20} />
            <span>Timetable</span>
          </a>
        </nav>
        <div className="p-4 border-t">
          <button
            onClick={handleLogout}
            className="flex items-center space-x-3 text-red-600 w-full p-3 rounded-lg hover:bg-red-50 transition"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="p-8">
            <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
