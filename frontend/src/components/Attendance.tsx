import React, { useEffect, useState } from 'react';
import { getAttendance, getAttendanceStatuses, getLessonHours, Attendance as AttendanceType } from '../services/api';
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
      <h2 className="text-3xl font-bold mb-8 text-zinc-100 tracking-tight">Obecność</h2>
      
      <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl hover:bg-zinc-800/50 transition-colors">
              <p className="text-zinc-500 text-xs font-medium uppercase tracking-wider mb-2">Frekwencja</p>
              <p className="text-3xl font-bold text-zinc-100">{rate.toFixed(1)}%</p>
          </div>
          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl hover:bg-zinc-800/50 transition-colors">
              <p className="text-zinc-500 text-xs font-medium uppercase tracking-wider mb-2">Dni obecne</p>
              <p className="text-3xl font-bold text-zinc-100">{presentCount}</p>
          </div>
           <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl hover:bg-zinc-800/50 transition-colors">
              <p className="text-zinc-500 text-xs font-medium uppercase tracking-wider mb-2">Wszystkie wpisy</p>
              <p className="text-3xl font-bold text-zinc-100">{total}</p>
          </div>
      </div>

      <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl overflow-hidden">
        <table className="w-full text-sm text-left text-zinc-400">
            <thead className="text-xs text-zinc-500 uppercase bg-zinc-950/50 border-b border-zinc-800">
                <tr>
                    <th className="px-6 py-4 font-medium">Data</th>
                    <th className="px-6 py-4 font-medium">Godzina lekcyjna</th>
                    <th className="px-6 py-4 font-medium">Status</th>
                </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/50">
                {attendance.map((record) => {
                    const statusName = statuses.get(record.status) || 'Nieznany';
                    const hourName = lessonHours.get(record.godzina_lekcyjna) || 'Nieznana godzina';
                    
                    let statusColor = 'text-zinc-400 bg-zinc-800/50 border-zinc-700';
                    if (isPresent(statusName)) statusColor = 'text-green-400 bg-green-900/20 border-green-900/30';
                    else if (isAbsent(statusName)) statusColor = 'text-red-400 bg-red-900/20 border-red-900/30';
                    else statusColor = 'text-yellow-400 bg-yellow-900/20 border-yellow-900/30';

                    return (
                        <tr key={record.id} className="hover:bg-zinc-900/30 transition-colors">
                            <td className="px-6 py-4 font-medium text-zinc-300 whitespace-nowrap">
                                {record.Data}
                            </td>
                            <td className="px-6 py-4">
                                {hourName}
                            </td>
                            <td className="px-6 py-4">
                                <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${statusColor}`}>
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
