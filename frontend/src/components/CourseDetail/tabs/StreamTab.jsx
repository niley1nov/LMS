// src/components/CourseDetail/tabs/StreamTab.jsx
import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";

// Imagine your API returns: course.announcements = [{ id, date, author, text }, …]
export default function StreamTab({ announcements = [] }) {
  if (!announcements.length) {
    return (
      <Typography sx={{ fontStyle: "italic", color: "text.disabled", mt: 2 }}>
        No announcements yet.
      </Typography>
    );
  }

  return (
    <Box>
      {announcements.map((ann) => (
        <Box key={ann.id} sx={{ mb: 3 }}>
          <Typography variant="subtitle2" color="text.secondary">
            {new Date(ann.date).toLocaleString()} — {ann.author}
          </Typography>
          <Typography sx={{ mt: 1 }}>{ann.text}</Typography>
          <Divider sx={{ mt: 2 }} />
        </Box>
      ))}
    </Box>
  );
}
