// src/App.js
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Navbar from "./components/Navbar.jsx";
import Sidebar from "./components/Sidebar.jsx";
import Home from "./components/Home.jsx";
import CourseDetail from "./components/CourseDetail.jsx";
import CreateCourseForm from "./components/CreateCourseForm.jsx";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <Router>
      <Navbar
        sidebarOpen={sidebarOpen}
        onToggleSidebar={() => setSidebarOpen((o) => !o)}
      />
      <Toolbar />
      <Box sx={{ display: "flex" }}>
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            bgcolor: (theme) => theme.palette.background.default,
            minHeight: (theme) => `calc(100vh - ${theme.mixins.toolbar.minHeight}px)`,
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/courses/new" element={<CreateCourseForm />} />
            <Route path="/courses/:id" element={<CourseDetail />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
