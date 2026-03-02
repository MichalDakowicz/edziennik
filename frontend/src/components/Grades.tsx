import React, { useEffect, useState } from 'react';
import { getGrades, getSubjects, Grade, Subject } from '../services/api';
import { getCurrentUser } from '../services/auth';
import { useNavigate } from 'react-router-dom';

const Grades: React.FC = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [subjectsMap, setSubjectsMap] = useState<Map<number, string>>(new Map());
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

        const [gradesData, subjectsData] = await Promise.all([
          getGrades(user.studentId),
          getSubjects()
        ]);

        console.log("Grades loaded:", gradesData);

        const subjects = new Map<number, string>();
        subjectsData.forEach((s: any) => subjects.set(s.id, s.nazwa)); // Check lowercase/uppercase from API response
        setSubjectsMap(subjects);
        setGrades(gradesData);
      } catch (err: any) {
        setError(err.message || 'Failed to load grades');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading grades...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  // Group by subject
  const subjectIds = Array.from(new Set(grades.map(g => g.przedmiot)));

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Grades</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {subjectIds.map(subjectId => {
          const subjectName = subjectsMap.get(subjectId) || `Subject ${subjectId}`;
          const subjectGrades = grades.filter(g => g.przedmiot === subjectId);
          
          const numericGrades = subjectGrades.map(g => ({ val: parseFloat(g.wartosc), weight: g.waga })).filter(g => !isNaN(g.val));
          const average = numericGrades.length > 0 
            ? numericGrades.reduce((sum, g) => sum + g.val * g.weight, 0) / numericGrades.reduce((sum, g) => sum + g.weight, 0)
            : 0;

          return (
            <div key={subjectId} className="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500 hover:shadow-lg transition">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold text-gray-700">{subjectName}</h3>
                <span className={`px-3 py-1 rounded-full text-sm font-bold ${average >= 4 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                  Avg: {average.toFixed(2)}
                </span>
              </div>
              <div className="space-y-3">
                {subjectGrades.map(grade => (
                  <div key={grade.id} className="flex justify-between items-center p-2 bg-gray-50 rounded-lg">
                    <div className="flex flex-col">
                      <span className="font-medium text-gray-800">{grade.opis || 'Grade'}</span>
                      <span className="text-xs text-gray-500">{new Date(grade.data_wystawienia).toLocaleDateString()} • Weight: {grade.waga}</span>
                    </div>
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-bold">
                      {grade.wartosc}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Grades;

