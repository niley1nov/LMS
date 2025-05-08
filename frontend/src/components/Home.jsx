// src/components/Home.js
import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext.jsx";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import CourseCard from "./CourseCard.jsx";
import { CoursesContext } from "../context/CoursesContext.jsx";

export default function Home() {
  const { courses, loading, error } = useContext(CoursesContext);

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Classroom
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {loading ? (
        <Typography>Loading courses…</Typography>
      ) : error ? (
        <Typography color="error">Error loading courses: {error}</Typography>
      ) : courses.length === 0 ? (
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
        <Grid container spacing={2}>
          {courses.map((course) => (
            <Grid item key={course.id}>
              <CourseCard course={course} />
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
}
