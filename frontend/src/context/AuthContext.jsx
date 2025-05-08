// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [initialized, setInitialized] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const fetchUserDetails = async () => {
    const response = await fetch(`${API_URL}/me`, { credentials: "include" });
    if (!response.ok) {
      throw new Error("Not authenticated");
    }
    return response.json();
  };

  // On mount, check session by calling /me
  useEffect(() => {
    fetchUserDetails()
      .then(data => setUser({ id: data.id, email: data.email, name: data.name }))
      .catch(() => setUser(null))
      .finally(() => setInitialized(true));
  }, [API_URL]);

  // Refresh user details after login or logout
  const refreshUser = () => {
    fetchUserDetails()
      .then(data => setUser({ id: data.id, email: data.email, name: data.name }))
      .catch(() => setUser(null));
  };

  const logout = async () => {
    try {
      await fetch(`${API_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
    } catch (error) {
      console.error("Logout failed:", error); // Optional: handle logout error
    } finally {
      setUser(null);
    }
  };

  // After login elsewhere, call setUser(...) then refreshUser()

  if (!initialized) return null;

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
