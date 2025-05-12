// src/components/CreateCourseForm.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// 1. Import Redux hooks and actions
import { useDispatch, useSelector } from 'react-redux';
import { createNewCourse, fetchUserCourses, clearCoursesError } from '../redux/coursesSlice'; // Assuming fetchUserCourses is the action to refresh
import { clearAuthError } from '../redux/authSlice'; // To clear any auth errors if relevant

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';

export default function CreateCourseForm() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  // Local error for form validation, Redux error for API submission
  const [formError, setFormError] = useState(null);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  // 2. Get state from Redux store
  const { user, isAuthenticated, loading: authLoading } = useSelector((state) => state.auth);
  const { loading: coursesSubmitting, error: coursesError } = useSelector((state) => state.courses);

  // Clear errors when component mounts or user changes
  useEffect(() => {
    dispatch(clearCoursesError());
    dispatch(clearAuthError()); // If auth errors could affect this form
    setFormError(null);
  }, [dispatch, user]);


  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormError(null); // Clear local form errors
    dispatch(clearCoursesError()); // Clear previous API submission errors

    if (!isAuthenticated) {
      setFormError("You must be logged in to create a course.");
      return;
    }

    if (!name.trim()) {
      setFormError("Course name is required.");
      return;
    }

    // Dispatch the createNewCourse thunk
    try {
      const resultAction = await dispatch(createNewCourse({ name, description }));
      if (createNewCourse.fulfilled.match(resultAction)) {
        // Successfully created course
        // Optionally, refresh the main courses list
        if (isAuthenticated) { // Ensure user is still authenticated before fetching their courses
            dispatch(fetchUserCourses());
        }
        navigate('/'); // Navigate to home page after successful creation
      } else {
        // Error handled by extraReducers, coursesError will be set in Redux state
        // If resultAction.payload contains a specific message, it's already in coursesError
        // setFormError(resultAction.payload || "Failed to create course."); // Or rely on coursesError from Redux
      }
    } catch (err) {
      // This catch block might not be strictly necessary if createNewCourse.rejected handles all errors
      // and sets them in the Redux state.
      console.error("Dispatch createNewCourse error:", err);
      // setFormError("An unexpected error occurred during submission."); // Or rely on coursesError
    }
  };

  // Handle auth loading state
  if (authLoading) {
    return (
        <Container maxWidth="sm" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
            <CircularProgress />
        </Container>
    );
  }

  if (!isAuthenticated) { // Check isAuthenticated instead of just user
    return (
        <Container maxWidth="sm" sx={{ mt: 4 }}>
            <Alert severity="warning">You must be logged in to create a course.</Alert>
            {/* Optionally, add a button to navigate to a login page */}
        </Container>
    );
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Create New Course
      </Typography>
      <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
        <TextField
          margin="normal"
          required
          fullWidth
          id="name"
          label="Course Name"
          name="name"
          autoComplete="off"
          autoFocus
          value={name}
          onChange={(e) => setName(e.target.value)}
          error={!!(formError && formError.toLowerCase().includes("name"))}
          helperText={ (formError && formError.toLowerCase().includes("name")) ? formError : "" }
        />
        <TextField
          margin="normal"
          fullWidth
          id="description"
          label="Course Description (Optional)"
          name="description"
          autoComplete="off"
          multiline
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        
        {/* Display local form errors or API submission errors from Redux state */}
        {(formError || coursesError) && (
          <Alert severity="error" sx={{ mt: 2, mb: 1 }}>
            {formError || coursesError}
          </Alert>
        )}

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          disabled={coursesSubmitting === 'pending' || authLoading}
        >
          {coursesSubmitting === 'pending' ? <CircularProgress size={24} color="inherit" /> : 'Create Course'}
        </Button>
      </Box>
    </Container>
  );
}