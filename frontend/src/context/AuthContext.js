// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [initialized, setInitialized] = useState(false);
  const [protectedMessage, setProtectedMessage] = useState('Loading protected data...');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // On mount, check session and load protected data
  useEffect(() => {
    fetch(`${API_URL}/protected`, { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error('Not authenticated');
        return res.json();
      })
      .then(data => {
        // parse user out of data.message if needed, or call /me
        setUser(prev => prev || { name: data.message.match(/^Hello ([^,]+)/)[1] });
        setProtectedMessage(data.message);
      })
      .catch(() => {
        setUser(null);
        setProtectedMessage('Not authenticated or error fetching data');
      })
      .finally(() => {
        setInitialized(true);
      });
  }, []);

  // whenever user logs in or out, re-fetch protected data
  const refreshProtected = () => {
    fetch(`${API_URL}/protected`, { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(data => setProtectedMessage(data.message))
      .catch(() => setProtectedMessage('Not authenticated or error fetching data'));
  };

  const logout = () => {
    fetch(`${API_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    }).then(() => {
      setUser(null);
      refreshProtected();
    });
  };

  // After login (in your Navbar’s handleSuccess), do:
  // setUser(data.user); refreshProtected();

  if (!initialized) return null;

  return (
    <AuthContext.Provider value={{
      user,
      setUser,
      logout,
      protectedMessage,
      refreshProtected
    }}>
      {children}
    </AuthContext.Provider>
  );
}
