// src/App.jsx
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux"; // Import Redux hooks
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Navbar from "./components/Navbar.jsx";
import Sidebar from "./components/Sidebar.jsx";
import Home from "./components/Home.jsx";
import CourseDetail from "./components/CourseDetail.jsx";
import CreateCourseForm from "./components/CreateCourseForm.jsx";
import CircularProgress from '@mui/material/CircularProgress';

import { fetchCurrentUser } from "./redux/authSlice"; // Import the thunk

function AppContent() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { initialAuthCheckDone, isAuthenticated } = useSelector((state) => state.auth);

  if (!initialAuthCheckDone) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

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
            minHeight: (theme) => `calc(100vh - ${theme.mixins.toolbar?.minHeight || '64'}px)`,
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            {/* Add protected routes concept later if needed based on isAuthenticated */}
            <Route path="/courses/new" element={<CreateCourseForm />} />
            <Route path="/courses/:id" element={<CourseDetail />} />
          </Routes>
        </Box>
      </Box>
    </>
  );
}

function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchCurrentUser()); // Fetch user on initial app load
  }, [dispatch]);

  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;