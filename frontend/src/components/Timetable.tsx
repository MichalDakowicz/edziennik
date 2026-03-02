import React, { useEffect, useState } from 'react';
import { getTimetablePlan, getTimetableEntries, getDaysOfWeek, getLessonHours, getSubjects, getZajecia, TimetableEntry, TimetablePlan, LessonHour, Subject, Zajecia } from '../services/api';
import { getCurrentUser } from '../services/auth';
import { useNavigate } from 'react-router-dom';

const Timetable: React.FC = () => {
  const [data, setData] = useState<Record<string, string>>({});
  const [days, setDays] = useState<string[]>([]);
  const [hours, setHours] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const user = getCurrentUser();
        if (!user || !user.classId || user.role !== 'uczen') {
            setError("No class assigned to user or not a student.");
            setLoading(false);
            return;
        }

        const [plans, daysData, hoursData, subjectsData, zajeciaData] = await Promise.all([
          getTimetablePlan(user.classId),
          getDaysOfWeek(),
          getLessonHours(),
          getSubjects(),
          getZajecia()
        ]);

        if (plans.length === 0) {
            setError("No active timetable found for your class.");
            setLoading(false);
            return;
        }

        // Use the latest plan (by date or ID)
        const currentPlan = plans.sort((a,b) => b.id - a.id)[0];
        const entries = await getTimetableEntries(currentPlan.id);

        // Prep lookups
        const subjectMap = new Map<number, string>();
        subjectsData.forEach((s: any) => subjectMap.set(s.id, s.nazwa));
        
        const zajeciaMap = new Map<number, string>();
        zajeciaData.forEach(z => {
            zajeciaMap.set(z.id, subjectMap.get(z.przedmiot) || 'Unknown Subject');
        });

        const dayMap = new Map<number, string>();
        daysData.sort((a: any, b: any) => a.Numer - b.Numer).forEach((d: any) => dayMap.set(d.id, d.Nazwa));
        setDays(Array.from(dayMap.values()));

        const hourMap = new Map<number, string>();
        hoursData.sort((a, b) => a.Numer - b.Numer).forEach(h => hourMap.set(h.id, `${h.CzasOd.substring(0,5)} - ${h.CzasDo.substring(0,5)}`));
        // We use index for row rendering, so let's keep array of hours strings
        setHours(hoursData.map(h => `${h.CzasOd.substring(0,5)} - ${h.CzasDo.substring(0,5)}`));

        // Build the grid data: "DayName-HourIndex" -> "SubjectName"
        // Note: HourIndex is tricky if IDs are not 0-based index. 
        // We better map "DayID-HourID" then translate to "DayName-HourIndex" for table.
        // Actually, let's map "DayName-HourIndex".
        // Find index of hour in sorted hoursData.
        
        const gridData: Record<string, string> = {};
        
        // Ensure we iterate over properly sorted hours to match the table rows
        const sortedHours = [...hoursData].sort((a, b) => a.Numer - b.Numer);

        entries.forEach((entry: any) => {
            const dayName = dayMap.get(entry.DzienTygodnia);
            // Find index in the sorted list which corresponds to table row index
            const hourIndex = sortedHours.findIndex(h => h.id === entry.godzina_lekcyjna);
            const subject = zajeciaMap.get(entry.zajecia);

            if (dayName && hourIndex !== -1 && subject) {
                gridData[`${dayName}-${hourIndex}`] = subject;
            }
        });

        setData(gridData);
      } catch (err: any) {
        setError(err.message || 'Failed to load timetable');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [navigate]);

   if (loading) return <div className="p-8 text-center text-gray-500">Loading timetable...</div>;
   if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="overflow-x-auto">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Weekly Timetable</h2>
      <div className="bg-white shadow-md rounded-lg overflow-hidden min-w-[800px]">
        <table className="w-full text-sm text-left text-gray-500">
          <thead className="text-xs text-gray-700 uppercase bg-gray-100">
            <tr>
              <th className="px-6 py-3 border-b">Hour</th>
              {days.map(day => (
                <th key={day} className="px-6 py-3 border-b text-center">{day}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {hours.map((hour, index) => (
              <tr key={index} className="bg-white border-b hover:bg-gray-50">
                <td className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50/50">
                  <div className="flex flex-col">
                    <span className="font-bold text-gray-800">Lesson {index + 1}</span>
                    <span className="text-xs text-gray-500">{hour}</span>
                  </div>
                </td>
                {days.map(day => {
                  const subject = data[`${day}-${index}`];
                  return (
                    <td key={day} className="px-6 py-4 text-center border-l border-gray-100">
                      {subject ? (
                        <div className="p-2 rounded bg-blue-100 text-blue-800 font-semibold shadow-sm">
                          {subject}
                        </div>
                      ) : (
                        <span className="text-gray-300">-</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Timetable;

