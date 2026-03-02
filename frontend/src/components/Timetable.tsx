import React, { useEffect, useState } from 'react';
import { getTimetablePlan, getTimetableEntries, getDaysOfWeek, getLessonHours, getSubjects, getZajecia } from '../services/api';
import { getCurrentUser } from '../services/auth';
import { useNavigate } from 'react-router-dom';

const Timetable: React.FC = () => {
  const [data, setData] = useState<Record<string, string>>({});
  const [days, setDays] = useState<string[]>([]);
  const [hours, setHours] = useState<string[]>([]);
  const [todayName, setTodayName] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const user = getCurrentUser();
        // Check if user is student
        if (!user || user.role !== 'uczen') {
            setError("Tylko uczniowie mają dostęp do planu lekcji.");
            setLoading(false);
            return;
        }
        if (!user.classId) {
            setError("Brak przypisanej klasy.");
            setLoading(false);
            return;
        }

        const [plans, daysData, hoursData, subjects, zajecia] = await Promise.all([
          getTimetablePlan(user.classId),
          getDaysOfWeek(),
          getLessonHours(),
          getSubjects(),
          getZajecia()
        ]);

        if (!plans || plans.length === 0) {
          setError("Brak aktywnego planu zajęć dla twojej klasy.");
          setLoading(false);
          return;
        }

        const currentPlan = plans.sort((a: any, b: any) => b.id - a.id)[0];
        const entries = await getTimetableEntries(currentPlan.id);

        // --- Prep Lookups ---
        const subjectMap = new Map<number, string>();
        // API might return {id, Nazwa} or {id, nazwa}
        subjects.forEach((s: any) => subjectMap.set(s.id, s.Nazwa || s.nazwa));

        const zajeciaMap = new Map<number, string>();
        zajecia.forEach((z: any) => {
          // z.przedmiot is an ID
          const subjName = subjectMap.get(z.przedmiot) || `Przedmiot ${z.przedmiot}`;
          zajeciaMap.set(z.id, subjName);
        });

        // Sort Days by Numer
        const sortedDays = daysData.sort((a: any, b: any) => a.Numer - b.Numer);
        setDays(sortedDays.map((d: any) => d.Nazwa));

        // Identify Today
        const jsDay = new Date().getDay(); 
        const dbDayNum = jsDay === 0 ? 7 : jsDay;
        const todayObj = sortedDays.find((d: any) => d.Numer === dbDayNum);
        if (todayObj) {
            setTodayName(todayObj.Nazwa);
        }

        // Sort Hours by Numer
        const sortedHours = hoursData.sort((a: any, b: any) => a.Numer - b.Numer);
        // We'll store formatted strings for display
        setHours(sortedHours.map((h: any) => `${h.CzasOd.substring(0, 5)} - ${h.CzasDo.substring(0, 5)}`));

        // --- Build Grid ---
        const grid: any = {};
        
        entries.forEach((entry: any) => {
          // Entry: { id, godzina_lekcyjna, dzien_tygodnia, zajecia }
          
          // Handle snake_case vs PascalCase for field names if API varies
          const dayId = entry.dzien_tygodnia || entry.DzienTygodnia;
          const hourId = entry.godzina_lekcyjna || entry.GodzinaLekcyjna;
          
          const dayObj = sortedDays.find((d: any) => d.id === dayId);
          const hourIndex = sortedHours.findIndex((h: any) => h.id === hourId);
          
          const subjectName = zajeciaMap.get(entry.zajecia);

          if (dayObj && hourIndex !== -1 && subjectName) {
              // Key format: "DayName-HourIndex" matches render loop
              grid[`${dayObj.Nazwa}-${hourIndex}`] = subjectName;
          }
        });

        setData(grid);
        setLoading(false);

      } catch (err: any) {
        console.error(err);
        setError(err.message || 'Nie udało się załadować planu lekcji');
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  if (loading) return (
    <div className="flex items-center justify-center h-64">
        <div className="text-zinc-500 text-lg animate-pulse">Ładowanie planu lekcji...</div>
    </div>
  );

  if (error) return (
    <div className="flex items-center justify-center h-64">
        <div className="text-red-400 bg-red-900/10 border border-red-900/20 px-6 py-4 rounded-xl">
            Error: {error}
        </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h2 className="text-3xl font-bold text-zinc-100 tracking-tight">Plan Lekcji</h2>
        <span className="text-zinc-500 text-sm bg-zinc-900/50 px-3 py-1 rounded-full border border-zinc-800">
            Klasa {getCurrentUser()?.classId ? '...' : ''}
        </span>
      </div>

      <div className="bg-zinc-900/30 border border-zinc-800 rounded-xl overflow-hidden shadow-sm overflow-x-auto">
        <table className="w-full text-sm text-left text-zinc-400 min-w-[800px]">
          <thead className="text-xs text-zinc-500 uppercase bg-zinc-950/50 border-b border-zinc-800">
            <tr>
              <th className="px-4 py-3 font-medium border-r border-zinc-800/50 w-24">Godzina</th>
              {days.map(day => (
                <th key={day} className={`px-4 py-3 font-medium border-r border-zinc-800/50 text-center last:border-0 ${day === todayName ? 'bg-blue-900/20 text-blue-200 ring-inset ring-2 ring-blue-500/20' : ''}`}>
                    {day}
                    {day === todayName && <span className="block text-[9px] text-blue-400 mt-0.5 normal-case font-normal">(Dzisiaj)</span>}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800/50">
            {hours.map((hourSpan, index) => {
               // index is the row index (0 = 1st lesson hour in sorted list)
               return (
              <tr key={index} className="group hover:bg-zinc-800/20 transition-colors">
                <td className="px-4 py-3 font-medium bg-zinc-950/20 border-r border-zinc-800/50 whitespace-nowrap">
                  <div className="flex flex-col">
                    <span className="font-bold text-zinc-300 text-xs">Lekcja {index + 1}</span>
                    <span className="text-[10px] text-zinc-600 font-mono mt-0.5">{hourSpan}</span>
                  </div>
                </td>
                {days.map(day => {
                  const subject = data[`${day}-${index}`];
                  const isToday = day === todayName;
                  return (
                    <td key={day} className={`px-2 py-2 text-center border-r border-zinc-800/50 last:border-0 align-top relative ${isToday ? 'bg-blue-900/5' : ''}`}>
                      {subject ? (
                        <div className={`p-2 rounded font-medium text-xs shadow-sm transition-colors h-full flex items-center justify-center ${isToday ? 'bg-blue-500/20 text-blue-200 border border-blue-500/40' : 'bg-blue-500/10 text-blue-300 border border-blue-500/20 group-hover:bg-blue-500/20'}`}>
                          {subject}
                        </div>
                      ) : (
                        <span className="text-zinc-800 select-none text-xs block mt-2">-</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            );
            })} 
          </tbody>
        </table>
      </div>
    </div>
  );
};
  
export default Timetable;

