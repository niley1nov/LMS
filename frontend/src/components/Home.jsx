// src/components/Home.jsx
import React from "react";
import { useGetCurrentUserQuery, useGetCoursesQuery } from "../redux/apiSlice";
import { useNavigate } from "react-router-dom";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Fab from "@mui/material/Fab";
import AddIcon from "@mui/icons-material/Add";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";
import CourseCard from "./CourseCard.jsx";

export default function Home() {
  const navigate = useNavigate();

  // Fetch current user
  const {
    data: user,
    isLoading: authLoading,
    isError: authError,
  } = useGetCurrentUserQuery();
  const isAuthenticated = Boolean(user) && !authError;

  // Fetch courses only if authenticated
  const {
    data: courses = [],
    isLoading: coursesLoading,
    isError: coursesError,
  } = useGetCoursesQuery(undefined, { skip: !isAuthenticated });

  // Show loader while auth or courses are loading
  if (authLoading || (isAuthenticated && coursesLoading)) {
    return (
      <Container
        sx={{
          py: 4,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "calc(100vh - 128px)",
        }}
      >
        <CircularProgress />
      </Container>
    );
  }

  const handleAddCourse = () => {
    navigate("/courses/new");
  };

  return (
    <Container sx={{ py: 4, position: "relative" }}>
      <Typography variant="h4" gutterBottom>
        {user ? `${user.name || user.email}'s Classroom` : "Classroom"}
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {coursesError ? (
        <Typography color="error" sx={{ textAlign: "center", mt: 4 }}>
          Error loading courses. Please try again.
        </Typography>
      ) : courses.length === 0 ? (
        <Box sx={{ textAlign: "center", mt: 8 }}>
          <Typography variant="h5" sx={{ mb: 2 }}>
            📚
          </Typography>
          <Typography variant="h6" sx={{ mt: 2, color: "text.secondary" }}>
            Your classroom is empty.
          </Typography>
          {isAuthenticated ? (
            <>
              <Typography sx={{ color: "text.secondary", mb: 2, mt: 1 }}>
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
          ) : (
            <Typography sx={{ color: "text.secondary", mt: 2 }}>
              Please log in to create and view your courses.
            </Typography>
          )}
        </Box>
      ) : (
        <Grid container spacing={3}>
          {courses.map((course) => (
            <Grid item key={course.id} xs={12} sm={6} md={4}>
              <CourseCard course={course} />
            </Grid>
          ))}
        </Grid>
      )}

      {isAuthenticated && (
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
