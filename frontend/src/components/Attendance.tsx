import React, { useEffect, useState } from 'react';
import { getAttendance, getAttendanceStatuses, getLessonHours, Attendance as AttendanceType } from '../services/api';
import { getCurrentUser } from '../services/auth';
import { useNavigate } from 'react-router-dom';

type StatusFilter = 'wszystkie' | 'nieobecnosc' | 'obecnosc' | 'spoznienie' | 'usprawiedliwienie' | 'zwolnienie';

const Attendance: React.FC = () => {
    const [attendance, setAttendance] = useState<AttendanceType[]>([]);
    const [statuses, setStatuses] = useState<Map<number, string>>(new Map());
    const [lessonHours, setLessonHours] = useState<Map<number, string>>(new Map());
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [statusFilter, setStatusFilter] = useState<StatusFilter>('wszystkie');
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
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

    // Kolory statusów: zwolnienie=niebieski, obecność=neutralny, usprawiedliwienie=zielony, nieobecność=czerwony, spóźnienie=żółty
    const getStatusColor = (status: string): string => {
        const s = status.toLowerCase();
        if (s.includes('nieobecn')) return 'text-red-400 bg-red-900/20 border-red-900/30';
        if (s.includes('zwoln')) return 'text-blue-400 bg-blue-900/20 border-blue-900/30';
        if (s.includes('usprawiedliw')) return 'text-green-400 bg-green-900/20 border-green-900/30';
        if (s.includes('spóźn') || s.includes('spozn')) return 'text-yellow-400 bg-yellow-900/20 border-yellow-900/30';
        if (s.includes('obecn')) return 'text-zinc-300 bg-zinc-800/50 border-zinc-700';
        return 'text-zinc-400 bg-zinc-800/50 border-zinc-700';
    };

    const getStatusName = (record: AttendanceType): string => {
        const s = record.status;
        if (s == null) return '';
        if (typeof s === 'object' && s !== null) {
            const o = s as { id?: number; Wartosc?: string; wartosc?: string };
            return (o.Wartosc ?? o.wartosc ?? statuses.get(o.id ?? 0) ?? '') as string;
        }
        return statuses.get(Number(s)) ?? '';
    };
    const total = attendance.length;
    // Jak na dashboardzie: obecność, spóźnienie i zwolnienie = „obecny”
    const isPresent = (status: string) => {
        const s = status.toLowerCase();
        return s.includes('obecn') || s.includes('spóźn') || s.includes('spozn') || s.includes('zwoln');
    };
    const presentCount = attendance.filter(a => isPresent(getStatusName(a))).length;
    const rate = total > 0 ? (presentCount / total) * 100 : null;
    const attendanceColor = rate === null ? 'text-zinc-400' : rate >= 80 ? 'text-green-400' : rate >= 50 ? 'text-amber-400' : 'text-red-400';

    const matchesStatusFilter = (statusName: string): boolean => {
        const s = statusName.toLowerCase();
        switch (statusFilter) {
            case 'nieobecnosc': return s.includes('nieobecn');
            case 'obecnosc': return s.includes('obecn') && !s.includes('nieobecn') && !s.includes('spóźn') && !s.includes('spozn');
            case 'spoznienie': return s.includes('spóźn') || s.includes('spozn');
            case 'usprawiedliwienie': return s.includes('usprawiedliw');
            case 'zwolnienie': return s.includes('zwoln');
            default: return true;
        }
    };
    const filteredAttendance = attendance.filter(a => matchesStatusFilter(getStatusName(a)));
    const filteredByDate = dateFrom || dateTo
        ? filteredAttendance.filter(r => {
            const d = r.Data;
            if (dateFrom && d < dateFrom) return false;
            if (dateTo && d > dateTo) return false;
            return true;
        })
        : filteredAttendance;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-8 text-zinc-100 tracking-tight">Obecność</h2>
      
      <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-zinc-900/50 border border-zinc-800 p-6 rounded-xl hover:bg-zinc-800/50 transition-colors">
              <p className="text-zinc-500 text-xs font-medium uppercase tracking-wider mb-2">Frekwencja</p>
              <p className={`text-3xl font-bold ${attendanceColor}`}>{rate !== null ? `${rate.toFixed(1)}%` : '—'}</p>
              {total === 0 && <p className="text-xs text-zinc-500 mt-1">Brak danych</p>}
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

      <div className="mb-4 flex flex-col sm:flex-row gap-4 flex-wrap">
          <div className="flex flex-wrap items-center gap-2">
              <span className="text-zinc-500 text-sm font-medium">Status:</span>
              {(['wszystkie', 'nieobecnosc', 'obecnosc', 'spoznienie', 'usprawiedliwienie', 'zwolnienie'] as const).map((f) => (
                  <button
                      key={f}
                      onClick={() => setStatusFilter(f)}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                          statusFilter === f
                              ? 'bg-blue-600 text-white'
                              : 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200'
                      }`}
                  >
                      {f === 'wszystkie' ? 'Wszystkie' : f.charAt(0).toUpperCase() + f.slice(1)}
                  </button>
              ))}
          </div>
          <div className="flex flex-wrap items-center gap-2">
              <label className="text-zinc-500 text-sm">Od:</label>
              <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-1.5 text-sm text-zinc-200"
              />
              <label className="text-zinc-500 text-sm">Do:</label>
              <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-1.5 text-sm text-zinc-200"
              />
              {(dateFrom || dateTo) && (
                  <button
                      type="button"
                      onClick={() => { setDateFrom(''); setDateTo(''); }}
                      className="text-zinc-500 hover:text-zinc-300 text-sm"
                  >
                      Wyczyść daty
                  </button>
              )}
          </div>
      </div>

      {(statusFilter !== 'wszystkie' || dateFrom || dateTo) && (
          <p className="text-sm text-zinc-500 mb-2">
              Pokazano {filteredByDate.length} z {total} wpisów
          </p>
      )}

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
                {filteredByDate.map((record) => {
                    const statusName = getStatusName(record) || 'Nieznany';
                    const hourName = lessonHours.get(record.godzina_lekcyjna) || 'Nieznana godzina';
                    const statusColor = getStatusColor(statusName);

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
