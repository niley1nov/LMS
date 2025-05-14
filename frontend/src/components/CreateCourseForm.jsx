// src/components/CreateCourseForm.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  useGetCurrentUserQuery,
  useCreateCourseMutation,
} from "../redux/apiSlice";

import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";

export default function CreateCourseForm() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [formError, setFormError] = useState(null);

  // RTK Query auth hook
  const {
    data: user,
    isLoading: authLoading,
    isError: authError,
  } = useGetCurrentUserQuery();
  const isAuthenticated = Boolean(user) && !authError;

  // RTK Query mutation hook
  const [createCourse, { isLoading: creating, error: createError }] =
    useCreateCourseMutation();

  // Show loader while checking auth
  if (authLoading) {
    return (
      <Container
        maxWidth="sm"
        sx={{ mt: 4, display: "flex", justifyContent: "center" }}
      >
        <CircularProgress />
      </Container>
    );
  }

  // If not authenticated, show warning
  if (!isAuthenticated) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <Alert severity="warning">
          You must be logged in to create a course.
        </Alert>
      </Container>
    );
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormError(null);

    if (!name.trim()) {
      setFormError("Course name is required.");
      return;
    }

    try {
      await createCourse({ name, description }).unwrap();
      navigate("/");
    } catch (err) {
      // err.data.detail for API error, err.error for network or other
      setFormError(err.data?.detail || err.error || "Failed to create course.");
    }
  };

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
          helperText={
            formError && formError.toLowerCase().includes("name")
              ? formError
              : ""
          }
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

        {(formError || createError) && (
          <Alert severity="error" sx={{ mt: 2, mb: 1 }}>
            {formError || createError?.data?.detail || createError?.error}
          </Alert>
        )}

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          disabled={creating}
        >
          {creating ? (
            <CircularProgress size={24} color="inherit" />
          ) : (
            "Create Course"
          )}
        </Button>
      </Box>
    </Container>
  );
}
