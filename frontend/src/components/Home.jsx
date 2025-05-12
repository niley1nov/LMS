// src/components/Home.jsx
import React, { useEffect } from "react"; // Removed useContext
// 1. Import Redux hooks and actions/thunks
import { useDispatch, useSelector } from "react-redux";
import { fetchUserCourses, clearCoursesError } from "../redux/coursesSlice"; // Assuming you have these
import { clearAuthError } from "../redux/authSlice"; // Optional: if auth errors are relevant here

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Fab from "@mui/material/Fab";
import AddIcon from "@mui/icons-material/Add";
import Button from "@mui/material/Button";
import CircularProgress from '@mui/material/CircularProgress';
import { useNavigate } from "react-router-dom";

import CourseCard from "./CourseCard.jsx";

export default function Home() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  // 2. Get state from Redux store
  const { user, isAuthenticated, loading: authLoading } = useSelector((state) => state.auth);
  const { items: courses, loading: coursesLoading, error: coursesError } = useSelector((state) => state.courses);

  // 3. Fetch courses when the component mounts or when the user/auth status changes
  useEffect(() => {
    // Clear previous errors on mount or when user changes
    dispatch(clearCoursesError());
    if (isAuthenticated) { // Only fetch courses if the user is authenticated
      dispatch(fetchUserCourses());
    }
  }, [dispatch, isAuthenticated]); // Re-fetch if isAuthenticated changes

  const isLoggedIn = isAuthenticated; // Use isAuthenticated from Redux

  const handleAddCourse = () => {
    navigate("/courses/new");
  };

  // Show a loading spinner if either authentication or courses are loading
  // Consider initialAuthCheckDone from authSlice if you have it, to avoid loading courses before auth is resolved
  if (authLoading === 'pending' || coursesLoading === 'pending') {
    return (
      <Container sx={{ py: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 'calc(100vh - 128px)' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container sx={{ py: 4, position: 'relative' }}>
      <Typography variant="h4" gutterBottom>
        {user ? `${user.name || user.email}'s Classroom` : "Classroom"}
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {coursesError ? (
        <Typography color="error" sx={{ textAlign: 'center', mt: 4 }}>
          Error loading courses: {typeof coursesError === 'string' ? coursesError : "An unknown error occurred."}
        </Typography>
      ) : courses.length === 0 ? (
        <Box sx={{ textAlign: "center", mt: 8 }}>
          <Typography variant="h5" component="div" sx={{ mb: 2 }}>
            📚
          </Typography>
          <Typography variant="h6" sx={{ mt: 2, color: "text.secondary" }}>
            Your classroom is empty.
          </Typography>
          {isLoggedIn ? (
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

      {/* Show FAB to add course if user is logged in */}
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
          disabled={authLoading === 'pending'} // Disable if auth is still resolving
        >
          <AddIcon />
        </Fab>
      )}
    </Container>
  );
}
