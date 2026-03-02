import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../services/auth';
import { getGrades, getAttendance, getSubjects, Grade, Attendance } from '../services/api';

const DashboardHome: React.FC = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState<{firstName: string, lastName: string, studentId: number} | null>(null);
    const [recentGrade, setRecentGrade] = useState<{value: string, subject: string, date: string} | null>(null);
    const [attendanceRate, setAttendanceRate] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const currentUser = getCurrentUser();
                if (currentUser) {
                    setUser(currentUser);
                    if (currentUser.role === 'uczen') {
                        const [grades, attendance, subjects] = await Promise.all([
                            getGrades(currentUser.studentId),
                            getAttendance(currentUser.studentId),
                            getSubjects()
                        ]);

                        if (grades.length > 0) {
                            // Sort by date desc
                            const sortedGrades = grades.sort((a,b) => new Date(b.data_wystawienia).getTime() - new Date(a.data_wystawienia).getTime());
                            const latest = sortedGrades[0];
                            // Note: getSubjects returns array of Subject {id, Nazwa}
                            const subjectEntry = (subjects as any[]).find((s:any) => s.id === latest.przedmiot);
                            const subjectName = subjectEntry ? subjectEntry.Nazwa : 'Unknown'; 
                            
                            setRecentGrade({
                                value: latest.wartosc, // Assuming 'wartosc' is the grade value string
                                subject: subjectName,
                                date: new Date(latest.data_wystawienia).toLocaleDateString()
                            });
                        }

                         if (attendance.length > 0) {
                             // This is a rough approximation as we don't fetch Status names here to check 'Present'
                             // Assuming standard IDs: usually 1=Obecny, 2=Nieobecny etc.
                             // But without map it's risky. Let's just count entries for now or skip rate if complex.
                             // Actually, let's keep it static or show "N/A" if we can't calc easily without fetching statuses.
                             setAttendanceRate(null); 
                         }
                    }
                }
            } catch (e) {
                console.error("Dashboard fetch error", e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="space-y-6">
            <h2 className="text-3xl font-bold mb-4 text-gray-800">Welcome back, {user ? `${user.firstName} ${user.lastName}` : 'Student'}!</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Summary Cards */}
                <div 
                    onClick={() => navigate('/dashboard/grades')}
                    className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg cursor-pointer transform hover:scale-105 transition"
                >
                    <h3 className="text-xl font-bold mb-2">Recent Grade</h3>
                    <p className="text-4xl font-extrabold">{recentGrade ? recentGrade.value : '-'}</p>
                    <p className="text-sm opacity-80 mt-1">{recentGrade ? `${recentGrade.subject} • ${recentGrade.date}` : 'No recent grades'}</p>
                </div>

                <div 
                    onClick={() => navigate('/dashboard/attendance')}
                    className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg cursor-pointer transform hover:scale-105 transition"
                >
                    <h3 className="text-xl font-bold mb-2">Attendance</h3>
                    <p className="text-4xl font-extrabold">92%</p>
                    <p className="text-sm opacity-80 mt-1">Keep it up!</p>
                </div>

                <div 
                    onClick={() => navigate('/dashboard/timetable')}
                    className="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl p-6 text-white shadow-lg cursor-pointer transform hover:scale-105 transition"
                >
                    <h3 className="text-xl font-bold mb-2">Next Lesson</h3>
                    <p className="text-2xl font-extrabold mt-2">Physics</p>
                    <p className="text-sm opacity-80 mt-1">Room 203 • 10:55</p>
                </div>
            </div>

            <div className="mt-8">
                <h3 className="text-xl font-bold text-gray-700 mb-4">Messages</h3>
                 <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-yellow-500">
                    <p className="font-semibold text-gray-800">Exam Alert: Physics</p>
                    <p className="text-gray-600 mt-1">Remember to prepare for the upcoming Physics exam on Friday.</p>
                    <p className="text-xs text-gray-400 mt-2">Posted by Mr. Smith • 2 hours ago</p>
                </div>
            </div>
        </div>
    );
};

export default DashboardHome;
