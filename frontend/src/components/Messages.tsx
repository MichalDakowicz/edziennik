import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCurrentUser } from '../services/auth';
import {
    getMessages,
    getTeachers,
    getUserProfile,
    patchMessage,
    Message
} from '../services/api';

const POLL_INTERVAL_MS = 30000;

type MessageWithSender = Message & { senderName: string };

const buildSenderMap = async (messages: Message[]): Promise<Map<number, string>> => {
    const userMap = new Map<number, string>();
    try {
        const teachers = await getTeachers();
        for (const t of teachers) {
            const u = t.user;
            if (u && typeof u === 'object' && 'id' in u) {
                const name = [u.first_name, u.last_name].filter(Boolean).join(' ').trim();
                userMap.set(u.id, name || (u.username as string) || `Użytkownik ${u.id}`);
            }
        }
        const senderIds = [...new Set(messages.map(msg => msg.nadawca))];
        for (const senderId of senderIds) {
            if (userMap.has(senderId)) continue;
            try {
                const profile = await getUserProfile(senderId);
                const name = [profile.first_name, profile.last_name].filter(Boolean).join(' ').trim();
                userMap.set(senderId, name || profile.username || `Użytkownik ${senderId}`);
            } catch {
                userMap.set(senderId, `Użytkownik ${senderId}`);
            }
        }
    } catch (e) {
        console.warn('Could not fetch sender names:', e);
    }
    return userMap;
};

const sortMessages = (messages: MessageWithSender[]): MessageWithSender[] =>
    [...messages].sort((a, b) => {
        if (a.przeczytana !== b.przeczytana) return a.przeczytana ? 1 : -1;
        return new Date(b.data_wyslania).getTime() - new Date(a.data_wyslania).getTime();
    });

const Messages: React.FC = () => {
    const navigate = useNavigate();
    const [messages, setMessages] = useState<MessageWithSender[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [messageModal, setMessageModal] = useState<MessageWithSender | null>(null);

    const fetchMessages = useCallback(async () => {
        const user = getCurrentUser();
        if (!user || user.role !== 'uczen') return;
        try {
            const raw = await getMessages(user.id);
            const userMap = await buildSenderMap(raw);
            const withSenders: MessageWithSender[] = raw.map(msg => ({
                ...msg,
                senderName: userMap.get(msg.nadawca) || `Użytkownik ${msg.nadawca}`
            }));
            setMessages(sortMessages(withSenders));
            setError('');
        } catch (e: any) {
            setError(e?.message || 'Nie udało się załadować wiadomości');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        const user = getCurrentUser();
        if (!user || user.role !== 'uczen') {
            navigate('/');
            return;
        }
        fetchMessages();
    }, [navigate, fetchMessages]);

    useEffect(() => {
        const user = getCurrentUser();
        if (!user || user.role !== 'uczen') return;
        const interval = setInterval(fetchMessages, POLL_INTERVAL_MS);
        return () => clearInterval(interval);
    }, [fetchMessages]);

    const openMessage = async (msg: MessageWithSender) => {
        setMessageModal(msg);
        if (!msg.przeczytana) {
            try {
                await patchMessage(msg.id, { przeczytana: true });
                const updated = { ...msg, przeczytana: true };
                setMessageModal(updated);
                setMessages(prev => sortMessages(prev.map(m => (m.id === msg.id ? updated : m))));
            } catch (e) {
                console.warn('Nie udało się oznaczyć wiadomości jako przeczytanej', e);
            }
        }
    };

    if (loading && messages.length === 0) {
        return <div className="p-8 text-center text-zinc-500">Ładowanie wiadomości...</div>;
    }
    if (error && messages.length === 0) {
        return <div className="p-8 text-center text-red-400">{error}</div>;
    }

    const unreadCount = messages.filter(m => !m.przeczytana).length;

    return (
        <div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
                <h2 className="text-3xl font-bold text-zinc-100 tracking-tight">Wiadomości</h2>
                {unreadCount > 0 && (
                    <span className="text-sm text-zinc-400 bg-zinc-800/50 px-3 py-1 rounded-full border border-zinc-700">
                        {unreadCount} nieprzeczytan{unreadCount === 1 ? 'a' : unreadCount >= 2 && unreadCount <= 4 ? 'e' : 'ych'}
                    </span>
                )}
            </div>

            <div className="space-y-4">
                {messages.length === 0 ? (
                    <div className="bg-zinc-900/30 rounded-xl border border-zinc-800 p-12 text-center text-zinc-500">
                        Brak wiadomości.
                    </div>
                ) : (
                    messages.map((msg) => (
                        <div
                            key={msg.id}
                            role="button"
                            tabIndex={0}
                            onClick={() => openMessage(msg)}
                            onKeyDown={(e) => e.key === 'Enter' && openMessage(msg)}
                            className="bg-zinc-900/30 rounded-xl border border-zinc-800 p-4 hover:border-zinc-700 transition-colors flex gap-4 items-start cursor-pointer"
                        >
                            <div className={`w-2 h-2 rounded-full mt-2 shrink-0 ${msg.przeczytana ? 'bg-zinc-700' : 'bg-blue-500'}`} />
                            <div className="min-w-0 flex-1">
                                <p className="font-semibold text-zinc-200 text-sm mb-1">{msg.temat}</p>
                                <p className="text-sm text-zinc-400 mb-1.5">
                                    <span className="text-zinc-500 font-medium">Od:</span>{' '}
                                    <span className="text-zinc-300">{msg.senderName}</span>
                                </p>
                                <p className="text-zinc-400 text-sm line-clamp-2">{msg.tresc}</p>
                                <p className="text-xs text-zinc-600 mt-2">
                                    {new Date(msg.data_wyslania).toLocaleString('pl-PL')}
                                </p>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {messageModal && (
                <div
                    className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60"
                    onClick={() => setMessageModal(null)}
                >
                    <div
                        className="bg-zinc-900 border border-zinc-700 rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-hidden flex flex-col"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="p-6 border-b border-zinc-800">
                            <h3 className="text-lg font-bold text-zinc-100 mb-2">{messageModal.temat}</h3>
                            <p className="text-sm text-zinc-400">
                                <span className="text-zinc-500 font-medium">Od:</span>{' '}
                                <span className="text-zinc-300">{messageModal.senderName}</span>
                            </p>
                            <p className="text-xs text-zinc-500 mt-1">
                                {new Date(messageModal.data_wyslania).toLocaleString('pl-PL')}
                            </p>
                        </div>
                        <div className="p-6 overflow-y-auto flex-1">
                            <p className="text-zinc-300 text-sm whitespace-pre-wrap">{messageModal.tresc}</p>
                        </div>
                        <div className="p-4 border-t border-zinc-800">
                            <button
                                type="button"
                                onClick={() => setMessageModal(null)}
                                className="w-full py-2 rounded-lg bg-zinc-800 text-zinc-200 hover:bg-zinc-700 font-medium"
                            >
                                Zamknij
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Messages;
