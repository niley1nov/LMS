// src/components/CreateUnitForm.jsx
import React, { useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  useGetCourseByIdQuery,
  useCreateUnitMutation,
} from "../redux/apiSlice";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Alert from "@mui/material/Alert";

// Define your unit types here (must match your backend Enum values):
const UnitTypeEnum = [
  "material",
  "assignment",
  "video",
  "quiz",
  "discussion",
  "external_link",
];

export default function CreateUnitForm() {
  const { moduleId, courseId } = useParams();
  const navigate = useNavigate();
  const { data: course, isLoading: courseLoading } =
    useGetCourseByIdQuery(courseId);
  const [title, setTitle] = useState("");
  const [unitType, setUnitType] = useState("material");
  const [content, setContent] = useState("");
  const [errors, setErrors] = useState([]);
  const [order, setOrder] = useState(0);

  const [createUnit, { isLoading: creating }] = useCreateUnitMutation();

  const nextOrder = useMemo(() => {
    const mod = course?.modules.find((m) => String(m.id) === moduleId);
    if (!mod || !mod.units?.length) return 1;
    return Math.max(...mod.units.map((u) => u.order || 0)) + 1;
  }, [course?.modules, moduleId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors([]);

    try {
      await createUnit({
        courseId,
        moduleId,
        title,
        unit_type: unitType,
        content,
        order: nextOrder,
      }).unwrap();

      // go back to Classwork tab
      navigate(`/courses/${courseId}`, { state: { initialTab: 1 } });
    } catch (err) {
      const detail = err.data?.detail;
      if (Array.isArray(detail)) {
        setErrors(detail.map((d) => d.msg));
      } else if (typeof detail === "string") {
        setErrors([detail]);
      } else {
        setErrors([err.error || "Unknown error creating unit"]);
      }
    }
  };

  if (courseLoading) {
    return (
      <Container sx={{ py: 4, textAlign: "center" }}>
        <Typography>Loading…</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        New Unit
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          fullWidth
          required
          sx={{ mb: 2 }}
        />

        <TextField
          select
          label="Type"
          value={unitType}
          onChange={(e) => setUnitType(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        >
          {UnitTypeEnum.map((type) => (
            <MenuItem key={type} value={type}>
              {type.replace("_", " ")}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Content / Link"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          fullWidth
          multiline
          rows={4}
          sx={{ mb: 2 }}
        />

        {errors.length > 0 && (
          <Box sx={{ mb: 2 }}>
            {errors.map((msg, i) => (
              <Alert key={i} severity="error" sx={{ mb: 1 }}>
                {msg}
              </Alert>
            ))}
          </Box>
        )}

        <Button type="submit" variant="contained" disabled={creating} fullWidth>
          {creating ? "Saving…" : "Create Unit"}
        </Button>
      </Box>
    </Container>
  );
}
