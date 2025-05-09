// src/context/CoursesContext.jsx
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { AuthContext } from './AuthContext.jsx';

export const CoursesContext = createContext();

export function CoursesProvider({ children }) {
  const { user } = useContext(AuthContext);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL;

  // useCallback to memoize fetchCourses, preventing unnecessary re-renders
  // if passed as a prop or used in other effects.
  const fetchCourses = useCallback(async () => {
    if (!user) {
      setCourses([]);
      setLoading(false);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null); // Reset error before new fetch
    try {
      const response = await fetch(`${API_URL}/courses`, {
        credentials: 'include',
      });
      if (!response.ok) {
        // Try to get error message from backend if available
        let errorMsg = `HTTP error ${response.status}`;
        try {
            const errorData = await response.json();
            errorMsg = errorData.detail || errorMsg;
        } catch (e) {
            // Ignore if response is not JSON
        }
        throw new Error(errorMsg);
      }
      const data = await response.json();
      setCourses(data);
    } catch (err) {
      setCourses([]); // Clear courses on error
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [API_URL, user]); // Dependencies for useCallback

  // useEffect to fetch courses when user or fetchCourses function changes
  useEffect(() => {
    fetchCourses();
  }, [fetchCourses]); // fetchCourses is now a stable dependency due to useCallback

  // Value provided by the context
  const contextValue = {
    courses,
    loading,
    error,
    refreshCourses: fetchCourses, // Expose fetchCourses as refreshCourses
  };

  return (
    <CoursesContext.Provider value={contextValue}>
      {children}
    </CoursesContext.Provider>
  );
}
