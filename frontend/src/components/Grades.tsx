import React, { useEffect, useState } from 'react';
import { getGrades, getSubjects, Grade } from '../services/api';
import { getCurrentUser } from '../services/auth';
import { useNavigate } from 'react-router-dom';

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
    if (isNaN(val)) return 'bg-zinc-900 border-zinc-800 text-zinc-100';
    
    if (val >= 5) return 'bg-emerald-900/20 text-emerald-400 border-emerald-900/30';
    if (val >= 4) return 'bg-green-900/20 text-green-400 border-green-900/30';
    if (val >= 3) return 'bg-yellow-900/20 text-yellow-400 border-yellow-900/30';
    if (val >= 2) return 'bg-orange-900/20 text-orange-400 border-orange-900/30';
    return 'bg-red-900/20 text-red-400 border-red-900/30';
};

type GradeModalState = { grade: Grade; subjectName: string } | null;

const Grades: React.FC = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [subjectsMap, setSubjectsMap] = useState<Map<number, string>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [gradeModal, setGradeModal] = useState<GradeModalState>(null);
  const [subjectSearch, setSubjectSearch] = useState('');
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

  if (loading) return <div className="p-8 text-center text-zinc-500">Ładowanie ocen...</div>;
  if (error) return <div className="p-8 text-center text-red-400">{error}</div>;

  // Group by subject
  const subjectIds = Array.from(new Set(grades.map(g => g.przedmiot)));
  const searchLower = subjectSearch.trim().toLowerCase();
  const filteredSubjectIds = searchLower
    ? subjectIds.filter(id => (subjectsMap.get(id) || `Przedmiot ${id}`).toLowerCase().includes(searchLower))
    : subjectIds;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6 text-zinc-100 tracking-tight">Oceny</h2>
      <div className="mb-6">
        <label htmlFor="subject-search" className="sr-only">Szukaj przedmiotu</label>
        <input
          id="subject-search"
          type="search"
          placeholder="Szukaj przedmiotu..."
          value={subjectSearch}
          onChange={(e) => setSubjectSearch(e.target.value)}
          className="w-full max-w-md bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2.5 text-zinc-200 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50"
        />
        {subjectSearch.trim() && (
          <p className="text-sm text-zinc-500 mt-2">
            Znaleziono {filteredSubjectIds.length} z {subjectIds.length} przedmiotów
          </p>
        )}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSubjectIds.map(subjectId => {
          const subjectName = subjectsMap.get(subjectId) || `Przedmiot ${subjectId}`;
          const subjectGrades = grades.filter(g => g.przedmiot === subjectId);
          
          const numericGrades = subjectGrades.map(g => ({ val: parseFloat(g.wartosc), weight: g.waga })).filter(g => !isNaN(g.val));
          const average = numericGrades.length > 0 
            ? numericGrades.reduce((sum, g) => sum + g.val * g.weight, 0) / numericGrades.reduce((sum, g) => sum + g.weight, 0)
            : 0;

          return (
            <div key={subjectId} className="bg-zinc-900/50 rounded-xl border border-zinc-800 p-6 hover:border-zinc-700 transition duration-200">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-xl font-semibold text-zinc-200 tracking-tight">{subjectName}</h3>
                <span className={`px-3 py-1 rounded-full text-xs font-medium border ${average >= 4 ? 'bg-green-900/20 text-green-400 border-green-900/30' : 'bg-yellow-900/20 text-yellow-400 border-yellow-900/30'}`}>
                  Śr: {average.toFixed(2)}
                </span>
              </div>
              <div className="space-y-3">
                {subjectGrades.map(grade => (
                  <div
                    key={grade.id}
                    role="button"
                    tabIndex={0}
                    onClick={() => setGradeModal({ grade, subjectName })}
                    onKeyDown={(e) => e.key === 'Enter' && setGradeModal({ grade, subjectName })}
                    className="flex justify-between items-center p-3 bg-zinc-950/50 border border-zinc-800/50 rounded-lg group hover:border-zinc-700 transition-colors cursor-pointer"
                  >
                    <div className="flex flex-col">
                      <span className="font-medium text-zinc-300 text-sm">{grade.opis || 'Ocena'}</span>
                      <span className="text-xs text-zinc-500">{new Date(grade.data_wystawienia).toLocaleDateString()} • Waga: {grade.waga}</span>
                    </div>
                    <div className={`flex items-center justify-center w-8 h-8 rounded-lg border font-bold text-sm transition-colors ${getGradeColor(grade.wartosc)}`}>
                      {formatGradeValue(grade.wartosc)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Grade detail modal */}
      {gradeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60" onClick={() => setGradeModal(null)}>
          <div className="bg-zinc-900 border border-zinc-700 rounded-xl shadow-xl max-w-md w-full p-6" onClick={e => e.stopPropagation()}>
            <h3 className="text-lg font-bold text-zinc-100 mb-4">Szczegóły oceny</h3>
            <dl className="space-y-3 text-sm">
              <div>
                <dt className="text-zinc-500 font-medium">Przedmiot</dt>
                <dd className="text-zinc-200">{gradeModal.subjectName}</dd>
              </div>
              <div className="flex items-center gap-3">
                <div>
                  <dt className="text-zinc-500 font-medium">Ocena</dt>
                  <dd>
                    <span className={`inline-flex items-center justify-center w-10 h-10 rounded-lg text-lg font-bold border ${getGradeColor(gradeModal.grade.wartosc)}`}>
                      {formatGradeValue(gradeModal.grade.wartosc)}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt className="text-zinc-500 font-medium">Waga</dt>
                  <dd className="text-zinc-200">{gradeModal.grade.waga}</dd>
                </div>
              </div>
              <div>
                <dt className="text-zinc-500 font-medium">Kategoria / Opis</dt>
                <dd className="text-zinc-300">{gradeModal.grade.opis || 'Ocena cząstkowa'}</dd>
              </div>
              <div>
                <dt className="text-zinc-500 font-medium">Data wystawienia</dt>
                <dd className="text-zinc-300">{new Date(gradeModal.grade.data_wystawienia).toLocaleDateString('pl-PL')}</dd>
              </div>
            </dl>
            <button type="button" onClick={() => setGradeModal(null)} className="mt-6 w-full py-2 rounded-lg bg-zinc-800 text-zinc-200 hover:bg-zinc-700 font-medium">
              Zamknij
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Grades;

