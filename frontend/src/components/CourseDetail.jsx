// src/components/CourseDetail.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";

export default function CourseDetail() {
  const { id } = useParams();
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
  const [course, setCourse] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/courses/${id}`, {
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setCourse(data))
      .catch((err) => setError(err.message));
  }, [API_URL, id]);

  if (error) {
    return (
      <Container sx={{ py: 4 }}>
        <Typography color="error">Error loading course: {error}</Typography>
      </Container>
    );
  }
  if (!course) {
    return (
      <Container sx={{ py: 4 }}>
        <Typography>Loading course…</Typography>
      </Container>
    );
  }

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        {course.name}
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Typography variant="body1" paragraph>
        {course.description}
      </Typography>

      <Box sx={{ mt: 4 }}>
        {/* TODO: render modules, lessons, quizzes, etc. */}
        <Typography color="text.secondary">
          (Course content will go here…)
        </Typography>
      </Box>
    </Container>
  );
}
