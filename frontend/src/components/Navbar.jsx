// src/components/Navbar.js
import React, { useContext, useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import { AuthContext } from "../context/AuthContext.jsx";
import ProfileDropdown from "./ProfileDropdown.jsx";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Avatar from "@mui/material/Avatar";

export default function Navbar({ sidebarOpen, onToggleSidebar }) {
  const { user, setUser, logout, refreshProtected } = useContext(AuthContext);
  const [anchorEl, setAnchorEl] = useState(null);
  const menuOpen = Boolean(anchorEl);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const handleLoginSuccess = ({ credential }) => {
    fetch(`${API_URL}/auth/google`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: credential }),
    })
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => {
        setUser(data.user);
        refreshProtected();
      })
      .catch(console.error);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
  };

  return (
    <AppBar position="fixed" sx={{ height: 60, justifyContent: "center" }}>
      <Toolbar sx={{ minHeight: 60, px: 2 }}>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onToggleSidebar}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, textAlign: "center" }}
        >
          Home
        </Typography>

        <Box>
          {!user ? (
            <GoogleLogin
              onSuccess={handleLoginSuccess}
              onError={(err) => console.error("Login Failed", err)}
            />
          ) : (
            <IconButton color="inherit" onClick={handleMenuOpen} size="small">
              <Avatar sx={{ bgcolor: "secondary.main", width: 32, height: 32 }}>
                {user.name[0]}
              </Avatar>
            </IconButton>
          )}
        </Box>
      </Toolbar>

      <ProfileDropdown
        anchorEl={anchorEl}
        open={menuOpen}
        onClose={handleMenuClose}
        onLogout={handleLogout}
      />
    </AppBar>
  );
}
