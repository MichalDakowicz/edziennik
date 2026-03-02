import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../services/auth';
import { 
    getGrades, getAttendance, getSubjects, getTimetablePlan, 
    getTimetableEntries, getLessonHours, getDaysOfWeek, getZajecia, 
    getAttendanceStatuses, getMessages,
    Grade, Message
} from '../services/api';

interface DashboardData {
    user: any;
    recentGrades: (Grade & { subjectName: string })[];
    averageGrade: number;
    attendanceRate: number;
    nextLesson: { subject: string; time: string; room?: string } | null;
    todayPlan: { time: string; subject: string; originalIndex: number }[];
    recentMessages: Message[];
}

const formatGradeValue = (value: string | number) => {
    const val = typeof value === 'string' ? parseFloat(value) : value;
    if (isNaN(val)) return value;

    if (val % 1 === 0.5) {
        return `${Math.floor(val)}+`;
    }
    if (val % 1 === 0.75) {
        return `${Math.ceil(val)}-`;
    }
    return val.toString();
};

const getGradeColor = (value: string | number) => {
    const val = typeof value === 'string' ? parseFloat(value) : value;
    if (isNaN(val)) return 'bg-zinc-800 text-zinc-100 border-zinc-700';
    
    if (val >= 5) return 'bg-emerald-900/20 text-emerald-400 border-emerald-900/30';
    if (val >= 4) return 'bg-green-900/20 text-green-400 border-green-900/30';
    if (val >= 3) return 'bg-yellow-900/20 text-yellow-400 border-yellow-900/30';
    if (val >= 2) return 'bg-orange-900/20 text-orange-400 border-orange-900/30';
    return 'bg-red-900/20 text-red-400 border-red-900/30';
};

const DashboardHome: React.FC = () => {
    const navigate = useNavigate();
    const [data, setData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const currentUser = getCurrentUser();
                if (!currentUser || currentUser.role !== 'uczen') {
                    setLoading(false);
                    return;
                }

                // 1. Start all fetches in parallel
                    const [
                    grades, 
                    attendance, 
                    subjects, 
                    plans, 
                    days, 
                    hours, 
                    zajecia,
                    statuses,
                    messages
                ] = await Promise.all([
                    getGrades(currentUser.studentId),
                    getAttendance(currentUser.studentId),
                    getSubjects(),
                    getTimetablePlan(currentUser.classId),
                    getDaysOfWeek(),
                    getLessonHours(),
                    getZajecia(),
                    getAttendanceStatuses(),
                    getMessages(currentUser.id) // Use currentUser.id (User PK) not studentId
                ]);

                // 2. Process Subjects Map
                const subjectMap = new Map<number, string>();
                subjects.forEach((s: any) => subjectMap.set(s.id, s.nazwa || s.Nazwa));

                // 3. Process Grades (Recent & Avg)
                const sortedGrades = grades.sort((a,b) => new Date(b.data_wystawienia).getTime() - new Date(a.data_wystawienia).getTime());
                const recentGrades = sortedGrades.slice(0, 5).map(g => ({
                    ...g,
                    subjectName: subjectMap.get(g.przedmiot) || 'Nieznany'
                }));

                const numericGrades = grades
                    .map(g => ({ val: parseFloat(g.wartosc), weight: g.waga }))
                    .filter(g => !isNaN(g.val));
                
                const averageGrade = numericGrades.length > 0
                    ? numericGrades.reduce((sum, g) => sum + g.val * g.weight, 0) / numericGrades.reduce((sum, g) => sum + g.weight, 0)
                    : 0;

                // 4. Process Attendance
                const statusMap = new Map<number, string>();
                statuses.forEach(s => statusMap.set(s.id, s.Wartosc));
                
                const isPresent = (status: string) => status.toLowerCase().includes('obecn') || status.toLowerCase().includes('spóźn');
                const presentCount = attendance.filter(a => isPresent(statusMap.get(a.status) || '')).length;
                const attendanceRate = attendance.length > 0 ? (presentCount / attendance.length) * 100 : 100;

                // 5. Process Timetable (Today's Plan & Next Lesson)
                let todayPlan: { time: string; subject: string; originalIndex: number }[] = [];
                let nextLesson = null;
                
                if (plans.length > 0) {
                    const currentPlan = plans.sort((a,b) => b.id - a.id)[0];
                    const entries = await getTimetableEntries(currentPlan.id);
                    
                    const jsDayToCheck = new Date().getDay(); 
                    const mapJsDayToDbNumer = (jsDay: number) => {
                         if(jsDay === 0) return 7; // Sunday
                         return jsDay;
                    };
                    const todayNumer = mapJsDayToDbNumer(jsDayToCheck);
                    
                    const todayDayObj = days.find((d: any) => d.Numer === todayNumer);

                    if (todayDayObj) {
                        const zajeciaMap = new Map<number, string>();
                        zajecia.forEach(z => zajeciaMap.set(z.id, subjectMap.get(z.przedmiot) || 'Unknown'));

                        const hoursMap = new Map<number, any>();
                        hours.forEach(h => hoursMap.set(h.id, h));

                        // Note: The API usually returns snake_case 'dzien_tygodnia' but verify
                        const todayEntries = entries.filter((e: any) => (e.dzien_tygodnia || e.DzienTygodnia) === todayDayObj.id);
                        
                        console.log('DEBUG: TodayEntries:', todayEntries);
                        console.log('DEBUG: ZajeciaMap:', zajeciaMap);
                        console.log('DEBUG: HoursMap:', hoursMap);

                        todayPlan = todayEntries.map((e: any) => {
                            const h = hoursMap.get(e.godzina_lekcyjna);
                            const timeStr = h ? `${h.CzasOd.toString().substring(0,5)}` : 'UNKNOWN';
                            const subj = zajeciaMap.get(e.zajecia) || 'Unknown';
                            return { time: timeStr, subject: subj, originalIndex: h?.Numer || 0 };
                        }).sort((a,b) => a.originalIndex - b.originalIndex);

                        // Find next lesson
                        const now = new Date();
                        const currentMinutes = now.getHours() * 60 + now.getMinutes();
                        
                        const upcoming = todayPlan.find(p => {
                             const [h, m] = p.time.split(':').map(Number);
                             return (h * 60 + m) > currentMinutes;
                        });

                        if (upcoming) {
                            nextLesson = { subject: upcoming.subject, time: upcoming.time };
                        }
                    }
                }

                setData({
                    user: currentUser,
                    recentGrades,
                    averageGrade,
                    attendanceRate,
                    nextLesson,
                    recentMessages: messages.slice(0, 3),
                    todayPlan
                });

            } catch (e) {
                console.error("Dashboard fetch error", e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return <div className="p-8 text-center text-zinc-500">Ładowanie pulpitu...</div>;
    }

    return (
        <div className="space-y-8">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-zinc-100 tracking-tight">
                    Witaj, {data?.user ? `${data.user.firstName}` : 'Uczniu'}!
                </h2>
                <span className="text-zinc-500 text-sm bg-zinc-900/50 px-3 py-1 rounded-full border border-zinc-800">
                    {new Date().toLocaleDateString('pl-PL', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
                </span>
            </div>
            
            {/* Top Stats Row */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div onClick={() => navigate('/dashboard/grades')} className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 cursor-pointer hover:border-zinc-700 transition group">
                    <div className="text-zinc-500 text-xs font-bold uppercase tracking-wider mb-1">Średnia ocen</div>
                    <div className="text-2xl font-bold text-zinc-100 group-hover:text-blue-400 transition-colors">
                        {data?.averageGrade?.toFixed(2) || '-'}
                    </div>
                </div>
                <div onClick={() => navigate('/dashboard/attendance')} className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 cursor-pointer hover:border-zinc-700 transition group">
                    <div className="text-zinc-500 text-xs font-bold uppercase tracking-wider mb-1">Frekwencja</div>
                    <div className={`text-2xl font-bold transition-colors ${data?.attendanceRate && data.attendanceRate < 80 ? 'text-red-400' : 'text-zinc-100 group-hover:text-green-400'}`}>
                        {data?.attendanceRate?.toFixed(1)}%
                    </div>
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="text-zinc-500 text-xs font-bold uppercase tracking-wider mb-1">Następna lekcja</div>
                    <div className="truncate text-zinc-100 font-semibold">
                        {data?.nextLesson ? data.nextLesson.subject : 'Koniec zajęć'}
                    </div>
                    {data?.nextLesson && <div className="text-xs text-zinc-500 mt-1">{data.nextLesson.time}</div>}
                </div>
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-4">
                    <div className="text-zinc-500 text-xs font-bold uppercase tracking-wider mb-1">Nowe wiadomości</div>
                    <div className="text-2xl font-bold text-zinc-100">1</div>
                </div>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                {/* Left Column: Timetable (Takes 1/3) */}
                <div className="lg:col-span-1 space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-xl font-bold text-zinc-200">Dzisiejszy plan</h3>
                        <button onClick={() => navigate('/dashboard/timetable')} className="text-xs text-blue-500 hover:text-blue-400 font-medium">Zobacz pełny</button>
                    </div>
                    <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl overflow-hidden">
                        {data?.todayPlan.length === 0 ? (
                             <div className="p-8 text-center text-zinc-500 text-sm">Brak zajęć na dzisiaj.</div>
                        ) : (
                            <div className="divide-y divide-zinc-800/50">
                                {data?.todayPlan.map((lesson, idx) => (
                                    <div key={idx} className="flex items-center p-3 hover:bg-zinc-800/30 transition-colors">
                                        <div className="w-12 text-xs text-zinc-500 font-mono">{lesson.time}</div>
                                        <div className="flex-1 font-medium text-sm text-zinc-300">{lesson.subject}</div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column: Grades (Takes 2/3) */}
                <div className="lg:col-span-2 space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-xl font-bold text-zinc-200">Ostatnie oceny</h3>
                        <button onClick={() => navigate('/dashboard/grades')} className="text-xs text-blue-500 hover:text-blue-400 font-medium">Zobacz wszystkie</button>
                    </div>
                    
                    <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl overflow-hidden">
                         {data?.recentGrades.length === 0 ? (
                             <div className="p-8 text-center text-zinc-500 text-sm">Brak ocen.</div>
                        ) : (
                        <table className="w-full text-sm text-left text-zinc-400">
                            <thead className="text-xs text-zinc-500 uppercase bg-zinc-950/50 border-b border-zinc-800">
                                <tr>
                                    <th className="px-6 py-3 font-medium">Przedmiot</th>
                                    <th className="px-6 py-3 font-medium">Ocena</th>
                                    <th className="px-6 py-3 font-medium hidden sm:table-cell">Kategoria</th>
                                    <th className="px-6 py-3 font-medium hidden sm:table-cell">Data</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-zinc-800/50">
                                {data?.recentGrades.map((grade) => (
                                    <tr key={grade.id} className="hover:bg-zinc-900/30 transition-colors">
                                        <td className="px-6 py-4 font-medium text-zinc-300">
                                            {grade.subjectName}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`inline-flex items-center justify-center w-8 h-8 rounded-lg text-sm font-bold border ${getGradeColor(grade.wartosc)}`}>
                                                {formatGradeValue(grade.wartosc)}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-xs text-zinc-500 hidden sm:table-cell">
                                            {grade.opis || 'Ocena cząstkowa'} <span className="opacity-50">• Waga: {grade.waga}</span>
                                        </td>
                                        <td className="px-6 py-4 text-xs text-zinc-500 hidden sm:table-cell">
                                            {new Date(grade.data_wystawienia).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        )}
                    </div>
                </div>
            </div>
            
            {/* Messages Section */}
            <div>
                 <h3 className="text-xl font-bold text-zinc-200 mb-4">Wiadomości</h3>
                 <div className="space-y-4">
                     {data?.recentMessages && data.recentMessages.length > 0 ? (
                         data.recentMessages.map((msg) => (
                            <div key={msg.id} className="bg-zinc-900/30 rounded-xl border border-zinc-800 p-4 hover:border-zinc-700 transition-colors flex gap-4 items-start">
                                <div className={`w-2 h-2 rounded-full mt-2 shrink-0 ${msg.przeczytana ? 'bg-zinc-700' : 'bg-blue-500'}`}></div>
                                <div>
                                    <div className="flex items-center gap-2 mb-1">
                                        <p className="font-semibold text-zinc-200 text-sm">{msg.temat}</p>
                                        {/* You might want to resolve sender name here if possible, for now static or ID */}
                                        <span className="text-[10px] text-zinc-600 border border-zinc-800 px-1.5 rounded">Od: {msg.nadawca}</span>
                                    </div>
                                    <p className="text-zinc-400 text-sm line-clamp-2">{msg.tresc}</p>
                                    <p className="text-xs text-zinc-600 mt-2">{new Date(msg.data_wyslania).toLocaleString()}</p>
                                </div>
                            </div>
                         ))
                     ) : (
                        <div className="bg-zinc-900/30 rounded-xl border border-zinc-800 p-8 text-center text-zinc-500 text-sm">
                            Brak nowych wiadomości.
                        </div>
                     )}
                 </div>
            </div>

        </div>
    );
};


export default DashboardHome;
