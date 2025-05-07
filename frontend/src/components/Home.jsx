// src/components/Home.js
import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext.jsx";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import CourseCard from "./CourseCard.jsx";

export default function Home() {
  const { protectedMessage } = useContext(AuthContext);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // --- TEST EMPTY-STATE: Uncomment the next two lines to simulate "no courses" ---
    // Promise.resolve([])
    //   .then(data => setCourses(data));

    // --- REAL FETCH: Comment out this block while testing empty-state ---
    fetch(`${API_URL}/courses`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setCourses(data))
      .catch((err) => setError(err.message));
  }, [API_URL]);

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Classroom
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {error && (
        <Typography color="error">Error loading courses: {error}</Typography>
      )}

      {error && (
        <Typography color="error">Error loading courses: {error}</Typography>
      )}

      {!error && courses.length === 0 ? (
        <Box sx={{ textAlign: "center", mt: 8 }}>
          <img src="/no-courses.jpg" alt="No courses" style={{ width: 200 }} />
          <Typography variant="h6" sx={{ mt: 2, color: "text.secondary" }}>
            No courses available yet.
          </Typography>
          <Typography sx={{ color: "text.secondary" }}>
            Check back later or contact the administrator.
          </Typography>
        </Box>
      ) : (
        <Grid container spacing={2} justifyContent="flex-start">
          {courses.map((course) => (
            <Grid item key={course.id}>
              <CourseCard course={course} />
            </Grid>
          ))}
        </Grid>
      )}

      {/* optional: access status below */}
      <Divider sx={{ my: 4 }} />
      <Typography variant="h6">Your Access Status</Typography>
      <Typography>{protectedMessage}</Typography>
    </Container>
  );
}
