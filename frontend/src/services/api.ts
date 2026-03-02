import { getAuthToken, refreshAccessToken, logout } from './auth';

const API_BASE_URL = '/api';

// --- Interfaces ---

export interface Subject {
    id: number;
    Nazwa: string;
    // Add other fields if needed
}

export interface Teacher {
    id: number;
    user: number; // User ID
    // Add filtering for name display if needed, but usually we just need ID
}

export interface Grade {
    id: number;
    wartosc: string; // Decimal string
    waga: number;
    opis: string;
    data_wystawienia: string;
    czy_punkty: boolean;
    czy_opisowa: boolean;
    czy_do_sredniej: boolean;
    uczen: number;
    nauczyciel: number;
    przedmiot: number;
}

export interface AttendanceStatus {
    id: number;
    Wartosc: string;
}

export interface Attendance {
    id: number;
    Data: string;
    uczen: number;
    godzina_lekcyjna: number;
    status: number; // Status ID
}

export interface LessonHour {
    id: number;
    Numer: number;
    CzasOd: string;
    CzasDo: string;
    CzasTrwania: number;
}

export interface TimetableEntry {
    id: number;
    dzien_tygodnia: number; // ID (Model field is snake_case)
    godzina_lekcyjna: number; // ID
    zajecia: number; // ID for Zajecia model
}

export interface Message {
    id: number;
    nadawca: number;
    odbiorca: number;
    temat: string;
    tresc: string;
    data_wyslania: string;
    przeczytana: boolean;
}

export interface Zajecia {
    id: number;
    przedmiot: number;
    nauczyciel: number;
}

export interface TimetablePlan {
    id: number;
    klasa: number;
    ObowiazujeOdDnia: string;
    wpisy: number[]; // Array of IDs
}

// --- Fetcher ---

const fetchWithAuth = async (endpoint: string, options: RequestInit = {}) => {
    let token = getAuthToken();
    const makeHeaders = (token: string | null) => ({
        'Content-Type': 'application/json',
        ...(token ? { 
            'Authorization': `Bearer ${token}`,
            'X-Authorization': `Bearer ${token}` // Duplicate for bypassing proxy stripping
        } : {}),
        ...options.headers,
    });

    let response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: makeHeaders(token),
        // Ensure credentials (cookies) are included if needed, though JWT is header-based
        // mode: 'cors', // default
    });

    if (!response.ok) {
        if (response.status === 401) {
            try {
                const errorBody = await response.clone().json();
                console.error("401 Error Body:", errorBody);
            } catch (e) {
                console.error("401 Error Body (text):", await response.clone().text());
            }

            console.warn("Unauthorized access, attempting to refresh token...");
            const newToken = await refreshAccessToken();
            if (newToken) {
                // Retry request with new token
                console.log("Token refreshed, retrying request...");
                response = await fetch(`${API_BASE_URL}${endpoint}`, {
                    ...options,
                    headers: makeHeaders(newToken),
                });
            } else {
                 console.error("Token refresh failed. Redirecting to login.");
                 logout();
                 window.location.href = '/'; 
                 throw new Error("Session expired. Please login again.");
            }
        }
        
        if (!response.ok) {
             throw new Error(`API Error: ${response.statusText}`);
        }
    }

    return response.json();
};

// --- API Methods ---

export const getSubjects = async (): Promise<Subject[]> => {
    return fetchWithAuth('/przedmioty/');
};

export const getGrades = async (studentId: number): Promise<Grade[]> => {
    return fetchWithAuth(`/oceny/?uczen=${studentId}`);
};

export const getAttendanceStatuses = async (): Promise<AttendanceStatus[]> => {
    return fetchWithAuth('/statusy/');
};

export const getAttendance = async (studentId: number): Promise<Attendance[]> => {
    return fetchWithAuth(`/frekwencja/?uczen_id=${studentId}`);
};

export const getLessonHours = async (): Promise<LessonHour[]> => {
    return fetchWithAuth('/godziny-lekcyjne/');
};

export const getTimetablePlan = async (classId: number): Promise<TimetablePlan[]> => {
    return fetchWithAuth(`/plany-zajec/?klasa_id=${classId}`);
};

export const getZajecia = async (): Promise<Zajecia[]> => {
    return fetchWithAuth('/zajecia/');
};

export const getTimetableEntries = async (planId: number): Promise<TimetableEntry[]> => {
    return fetchWithAuth(`/plan-wpisy/?plan_id=${planId}`);
};

export const getMessages = async (userId: number): Promise<Message[]> => {
    return fetchWithAuth(`/wiadomosci/?odbiorca=${userId}`);
};

export const getDaysOfWeek = async (): Promise<{id: number, Nazwa: string, Numer: number}[]> => {
    return fetchWithAuth('/dni-tygodnia/');
};
