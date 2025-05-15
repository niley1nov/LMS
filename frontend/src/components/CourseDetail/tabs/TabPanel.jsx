// src/components/CourseDetail/tabs/TabPanel.jsx
import React from "react";
import Box from "@mui/material/Box";

export default function TabPanel({ children, value, index }) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ mt: 2 }}>{children}</Box>}
    </div>
  );
}
