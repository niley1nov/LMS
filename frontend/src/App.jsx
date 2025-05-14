// src/App.jsx
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Navbar from "./components/Navbar.jsx";
import Sidebar from "./components/Sidebar.jsx";
import Home from "./components/Home.jsx";
import CourseDetail from "./components/CourseDetail.jsx";
import CreateCourseForm from "./components/CreateCourseForm.jsx";
import CircularProgress from "@mui/material/CircularProgress";
import { useGetCurrentUserQuery } from "./redux/apiSlice";

function AppContent() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { data: user, isLoading, isError } = useGetCurrentUserQuery();

  if (isLoading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  const isAuthenticated = Boolean(user) && !isError;

  return (
    <>
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
            minHeight: (theme) =>
              `calc(100vh - ${theme.mixins.toolbar?.minHeight || "64"}px)`,
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            {/*
              Later you can wrap the next two in a `<RequireAuth>`
              that redirects if !isAuthenticated
            */}
            <Route path="/courses/new" element={<CreateCourseForm />} />
            <Route path="/courses/:id" element={<CourseDetail />} />
          </Routes>
        </Box>
      </Box>
    </>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
