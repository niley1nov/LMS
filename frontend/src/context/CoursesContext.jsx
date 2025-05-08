// src/context/CoursesContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthContext } from './AuthContext.jsx';

export const CoursesContext = createContext();

export function CoursesProvider({ children }) {
  const { user } = useContext(AuthContext);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL;

  useEffect(() => {
    // console.log(user); // You can remove this debugging log
    if (!user) {
      setCourses([]);
      setLoading(false);
      setError(null); // Good, already resetting error
      return;
    }

    setLoading(true);
    // CHANGE HERE: Remove the user_id query parameter
    fetch(`${API_URL}/courses`, { // No more ?user_id=${user.id}
      credentials: 'include', // This is important for sending session cookies
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error ${res.status}`); // More descriptive error
        return res.json();
      })
      .then(data => {
        setCourses(data);
        setError(null);
      })
      .catch(err => {
        setCourses([]); // Clear courses on error
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [API_URL, user]); // Dependencies are correct: re-fetch if API_URL or user changes

  return (
    <CoursesContext.Provider value={{ courses, loading, error }}>
      {children}
    </CoursesContext.Provider>
  );
}