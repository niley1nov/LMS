// src/components/CreateCourseForm.jsx
import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { CoursesContext } from '../context/CoursesContext.jsx';
import { AuthContext } from '../context/AuthContext.jsx'; // To ensure user is logged in

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert'; // For displaying errors
import CircularProgress from '@mui/material/CircularProgress'; // For loading state

const API_URL = process.env.REACT_APP_API_URL;

export default function CreateCourseForm() {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  
  const navigate = useNavigate();
  const { refreshCourses } = useContext(CoursesContext);
  const { user } = useContext(AuthContext); // Get user to ensure they are logged in

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null); // Clear previous errors

    if (!name.trim()) {
      setError("Course name is required.");
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch(`${API_URL}/courses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, description }),
        credentials: 'include', // Important for sending session cookies
      });

      const responseData = await response.json(); // Try to parse JSON regardless of response.ok

      if (!response.ok) {
        // Use error detail from backend if available, otherwise a generic message
        throw new Error(responseData.detail || `Error: ${response.status} ${response.statusText}`);
      }
      
      // Successfully created course
      await refreshCourses(); // Refresh the courses list in the context
      navigate('/'); // Navigate to home page after successful creation

    } catch (err) {
      setError(err.message || "An unexpected error occurred. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  // If no user, ideally this page shouldn't be accessible or should show a message.
  // Route protection is a more robust way to handle this.
  if (!user) {
    return (
        <Container maxWidth="sm" sx={{ mt: 4 }}>
            <Alert severity="warning">You must be logged in to create a course.</Alert>
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
          error={!!(error && error.toLowerCase().includes("name"))} // Basic error highlighting
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
        
        {error && (
          <Alert severity="error" sx={{ mt: 2, mb: 1 }}>
            {error}
          </Alert>
        )}

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          disabled={submitting}
        >
          {submitting ? <CircularProgress size={24} color="inherit" /> : 'Create Course'}
        </Button>
      </Box>
    </Container>
  );
}
