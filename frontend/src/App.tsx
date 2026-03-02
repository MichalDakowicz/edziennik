import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login.tsx';
import Layout from './components/Layout.tsx';
import DashboardHome from './components/DashboardHome.tsx';
import Grades from './components/Grades.tsx';
import Attendance from './components/Attendance.tsx';
import Timetable from './components/Timetable.tsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        
        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={<Layout />}>
          <Route index element={<DashboardHome />} />
          <Route path="grades" element={<Grades />} />
          <Route path="attendance" element={<Attendance />} />
          <Route path="timetable" element={<Timetable />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
