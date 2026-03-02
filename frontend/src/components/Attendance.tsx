import React, { useEffect, useState } from 'react';
import { getAttendance, getAttendanceStatuses, getLessonHours, Attendance as AttendanceType, AttendanceStatus, LessonHour } from '../services/api';
import { getCurrentUser } from '../services/auth';
import { useNavigate } from 'react-router-dom';

const Attendance: React.FC = () => {
    const [attendance, setAttendance] = useState<AttendanceType[]>([]);
    const [statuses, setStatuses] = useState<Map<number, string>>(new Map());
    const [lessonHours, setLessonHours] = useState<Map<number, string>>(new Map());
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const user = getCurrentUser();
                if (!user || user.role !== 'uczen') {
                   navigate('/');
                   return;
                }

                const [attendanceData, statusData, hoursData] = await Promise.all([
                    getAttendance(user.studentId),
                    getAttendanceStatuses(),
                    getLessonHours()
                ]);

                const statusMap = new Map<number, string>();
                statusData.forEach(s => statusMap.set(s.id, s.Wartosc));
                setStatuses(statusMap);

                const hoursMap = new Map<number, string>();
                hoursData.forEach(h => hoursMap.set(h.id, `${h.Numer}. ${h.CzasOd} - ${h.CzasDo}`));
                setLessonHours(hoursMap);

                setAttendance(attendanceData);
            } catch (err: any) {
                setError(err.message || 'Failed to load attendance');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [navigate]);

    if (loading) return <div className="p-8 text-center text-gray-500">Loading attendance...</div>;
    if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

    // Generate stats
    const total = attendance.length;
    // We need to know which status means "Present" etc. Ideally backend gives this info or we hardcode based on "Wartosc"
    // For PoC let's guess based on string content
    const isPresent = (status: string) => status.toLowerCase().includes('obecn') || status.toLowerCase().includes('spóźn');
    const isAbsent = (status: string) => status.toLowerCase().includes('nieobecn');
    
    const presentCount = attendance.filter(a => isPresent(statuses.get(a.status) || '')).length;
    const rate = total > 0 ? (presentCount / total) * 100 : 100;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Attendance</h2>
      
      <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-lg shadow border-l-4 border-purple-500">
              <p className="text-gray-500 text-sm">Attendance Rate</p>
              <p className="text-2xl font-bold">{rate.toFixed(1)}%</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow border-l-4 border-green-500">
              <p className="text-gray-500 text-sm">Present Days</p>
              <p className="text-2xl font-bold">{presentCount}</p>
          </div>
           <div className="bg-white p-4 rounded-lg shadow border-l-4 border-red-500">
              <p className="text-gray-500 text-sm">Total Entries</p>
              <p className="text-2xl font-bold">{total}</p>
          </div>
      </div>

      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <table className="w-full text-sm text-left text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                    <th className="px-6 py-3">Date</th>
                    <th className="px-6 py-3">Lesson Time</th>
                    <th className="px-6 py-3">Status</th>
                </tr>
            </thead>
            <tbody>
                {attendance.map((record) => {
                    const statusName = statuses.get(record.status) || 'Unknown';
                    const hourName = lessonHours.get(record.godzina_lekcyjna) || 'Unknown Time';
                    
                    let statusColor = 'text-gray-800 bg-gray-100';
                    if (isPresent(statusName)) statusColor = 'text-green-800 bg-green-100';
                    else if (isAbsent(statusName)) statusColor = 'text-red-800 bg-red-100';
                    else statusColor = 'text-yellow-800 bg-yellow-100';

                    return (
                        <tr key={record.id} className="bg-white border-b hover:bg-gray-50">
                            <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap">
                                {record.Data}
                            </td>
                            <td className="px-6 py-4">
                                {hourName}
                            </td>
                            <td className="px-6 py-4">
                                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusColor}`}>
                                    {statusName}
                                </span>
                            </td>
                        </tr>
                    );
                })}
            </tbody>
        </table>
      </div>
    </div>
  );
};

export default Attendance;
