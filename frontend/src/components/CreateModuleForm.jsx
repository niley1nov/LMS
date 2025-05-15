// src/components/CreateModuleForm.jsx
import React, { useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { useGetCourseByIdQuery, useCreateModuleMutation } from "../redux/apiSlice";

export default function CreateModuleForm() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [order, setOrder] = useState(0);
  const [serverErrors, setServerErrors] = useState([]);
  const [createModule, { isLoading }] = useCreateModuleMutation();

  const { data: course, isFetching: courseLoading } =
    useGetCourseByIdQuery(courseId);

  const nextOrder = useMemo(() => {
    if (!course?.modules?.length) return 1;
    return Math.max(...course.modules.map((m) => m.order ?? 0)) + 1;
  }, [course?.modules]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerErrors([]);
    try {
      await createModule({ courseId, title, description, order: nextOrder }).unwrap();
      navigate(`/courses/${courseId}`, { state: { initialTab: 1 } });
    } catch (err) {
      console.error("createModule error:", err);
      // If Pydantic returned a detail array, pull out the .msg fields
      if (Array.isArray(err.data?.detail)) {
        setServerErrors(err.data.detail.map((d) => d.msg));
      } else if (typeof err.data?.detail === "string") {
        setServerErrors([err.data.detail]);
      } else {
        setServerErrors([err.error || "Unknown error creating module"]);
      }
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        New Module
      </Typography>
      <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 2 }}>
        <TextField
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          fullWidth
          required
          sx={{ mb: 2 }}
        />
        <TextField
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          fullWidth
          multiline
          rows={3}
          sx={{ mb: 2 }}
        />
        {serverErrors.length > 0 && (
          <Box sx={{ mb: 2 }}>
            {serverErrors.map((msg, i) => (
              <Typography key={i} color="error">
                {msg}
              </Typography>
            ))}
          </Box>
        )}
        <Button
          type="submit"
          variant="contained"
          disabled={isLoading}
          fullWidth
        >
          {isLoading ? "Saving…" : "Create Module"}
        </Button>
      </Box>
    </Container>
  );
}
