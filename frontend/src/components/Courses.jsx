import React, { useEffect, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/courses`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setCourses(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;
  if (courses.length === 0) return <p>Loading courses…</p>;

  return (
    <section id="courses">
      <h2>Available Courses</h2>
      <ul>
        {courses.map((c) => (
          <li key={c.id} style={{ margin: "10px 0" }}>
            <strong>{c.name}</strong>
            <p>{c.description}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
