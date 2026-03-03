// src/services/auth.ts
import { jwtDecode } from 'jwt-decode';

export interface TokenPayload {
  user_id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'uczen' | 'nauczyciel' | 'admin' | string;
  uczen_id?: number;
  klasa_id?: number;
  nauczyciel_id?: number;
  exp: number;
}

const API_BASE_URL = 'https://dziennik.polandcentral.cloudapp.azure.com/api';

export const login = async (username: string, password: string): Promise<string | null> => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Invalid credentials');
      }
      throw new Error(`Authentication failed: ${response.statusText}`);
    }

    const data = await response.json();
    const token = data.access; // Assuming access token field is 'access'
    
    // Validate role for students
    const decoded: TokenPayload = jwtDecode(token);
    
    if (decoded.role !== 'uczen') {
        throw new Error('Only students can access this portal');
    }

    localStorage.setItem('access_token', token);
    localStorage.setItem('refresh_token', data.refresh); // Store refresh token securely ideally
    
    // Store user info
    localStorage.setItem('user', JSON.stringify({
        id: decoded.user_id,
        firstName: decoded.first_name,
        lastName: decoded.last_name,
        email: decoded.email,
        username: decoded.username,
        role: decoded.role,
        studentId: decoded.uczen_id,
        classId: decoded.klasa_id
    }));

    return token;
  } catch (error) {
    throw error;
  }
};

export const refreshAccessToken = async (): Promise<string | null> => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        console.warn("No refresh token found");
        return null;
    }

    try {
        console.log("Refreshing token...");
        const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!response.ok) {
            console.error("Refresh token failed with status:", response.status);
            // const errorText = await response.text();
            // console.error("Error details:", errorText);
            logout();
            return null;
        }

        const data = await response.json();
        // Check if access token is present
        if (!data.access) {
            console.error("Refresh response missing access token:", data);
            logout();
            return null;
        }

        const newAccessToken = data.access;
        // Optionally update refresh token if rotation is enabled and new one provided
        if (data.refresh) {
            localStorage.setItem('refresh_token', data.refresh);
        }
        
        localStorage.setItem('access_token', newAccessToken);
        return newAccessToken;
    } catch (e) {
        console.error("Refresh token exception:", e);
        logout();
        return null; 
    }
}

export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
}

export const getAuthToken = () => {
    return localStorage.getItem('access_token');
}

export const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

export const isAuthenticated = () => {
    // Simple check, in a real app you verify token expiry as well
    const token = getAuthToken();
    if (!token) return false;

    try {
        const decoded: TokenPayload = jwtDecode(token);
        return decoded.exp * 1000 > Date.now();
    } catch {
        return false;
    }
}
