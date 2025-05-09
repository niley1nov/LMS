// src/components/Home.jsx
import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext.jsx";
import { CoursesContext } from "../context/CoursesContext.jsx";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Fab from "@mui/material/Fab";
import AddIcon from "@mui/icons-material/Add";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";

import CourseCard from "./CourseCard.jsx";

export default function Home() {
  const { courses, loading, error } = useContext(CoursesContext);
  const { user } = useContext(AuthContext); // Get the user to ensure someone is logged in
  const navigate = useNavigate();

  // For now, any logged-in user can attempt to create a course.
  // The backend will handle actual creation.
  // We just need to make sure a user is logged in to show the button.
  const isLoggedIn = !!user;

  const handleAddCourse = () => {
    // Navigate to the page/modal for creating a new course
    // This route should lead to a form component for creating a course.
    navigate("/courses/new");
  };

  return (
    <Container sx={{ py: 4, position: 'relative' }}>
      <Typography variant="h4" gutterBottom>
        Classroom
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {loading ? (
        <Typography>Loading courses…</Typography>
      ) : error ? (
        <Typography color="error">Error loading courses: {error}</Typography>
      ) : courses.length === 0 ? ( // This block is for when there are NO courses
        <Box sx={{ textAlign: "center", mt: 8 }}>
          <img src="/no-courses.jpg" alt="No courses" style={{ width: 200 }} />
          <Typography variant="h6" sx={{ mt: 2, color: "text.secondary" }}>
            Your classroom is empty.
          </Typography>
          {isLoggedIn && ( // Show create button only if logged in
            <>
              <Typography sx={{ color: "text.secondary", mb: 2 }}>
                Get started by adding your first course!
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddCourse}
              >
                Create New Course
              </Button>
            </>
          )}
          {!isLoggedIn && ( // Prompt to log in if no courses and not logged in
             <Typography sx={{ color: "text.secondary", mt: 2 }}>
                Log in to create and view courses.
            </Typography>
          )}
        </Box>
      ) : ( // This block is for when there ARE courses
        <Grid container spacing={2}>
          {courses.map((course) => (
            <Grid item key={course.id} xs={12} sm={6} md={4} lg={3}>
              <CourseCard course={course} />
            </Grid>
          ))}
        </Grid>
      )}

      {/* Show FAB to add course if user is logged in, regardless of course count */}
      {isLoggedIn && (
        <Fab
          color="primary"
          aria-label="add course"
          onClick={handleAddCourse}
          sx={{
            position: "fixed",
            bottom: (theme) => theme.spacing(4),
            right: (theme) => theme.spacing(4),
          }}
        >
          <AddIcon />
        </Fab>
      )}
    </Container>
  );
}