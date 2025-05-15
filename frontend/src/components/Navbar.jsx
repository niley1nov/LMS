// src/components/Navbar.jsx
import React, { useState } from "react";
import {
  GoogleOAuthProvider,
  GoogleLogin,
  googleLogout,
} from "@react-oauth/google";
import { useDispatch } from "react-redux";
import {
  api,
  useGetCurrentUserQuery,
  useLoginWithGoogleMutation,
  useLogoutUserMutation,
  useGetCourseByIdQuery,
} from "../redux/apiSlice";
import { useNavigate, Link as RouterLink, useMatch } from "react-router-dom";

import ProfileDropdown from "./ProfileDropdown.jsx";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Breadcrumbs from "@mui/material/Breadcrumbs";
import Link from "@mui/material/Link";
import Avatar from "@mui/material/Avatar";
import CircularProgress from "@mui/material/CircularProgress";

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;
if (!GOOGLE_CLIENT_ID) {
  console.error(
    "ERROR: REACT_APP_GOOGLE_CLIENT_ID is not defined. Google Login will not work."
  );
}

export default function Navbar({ sidebarOpen, onToggleSidebar }) {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const menuOpen = Boolean(anchorEl);
  const dispatch = useDispatch();

  // RTK Query hooks
  const {
    data: user,
    isLoading: authLoading,
    isError: authError,
  } = useGetCurrentUserQuery();
  const isAuthenticated = Boolean(user) && !authError;

  const [loginWithGoogle, { isLoading: loginLoading }] =
    useLoginWithGoogleMutation();
  const [logoutUser] = useLogoutUserMutation();

  // Breadcrumb: match /courses/:id
  const courseMatch = useMatch("/courses/:id");
  let courseName;
  const { data: course, isLoading: courseLoading } = useGetCourseByIdQuery(
    courseMatch?.params.id ?? "",
    {
      skip: !courseMatch,
    }
  );
  if (courseMatch) {
    courseName = course?.name;
  }

  const handleGoogleLoginSuccess = async (credentialResponse) => {
    if (credentialResponse.credential) {
      try {
        await loginWithGoogle(credentialResponse.credential).unwrap();
      } catch (error) {
        console.error("Backend login failed after Google sign-in:", error);
      }
    } else {
      console.error("Google login succeeded but no credential received.");
    }
  };

  const handleGoogleLoginError = (error) => {
    console.error("Google Login Failed:", error);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleMenuClose = () => setAnchorEl(null);

  const handleLogout = async () => {
    try {
      await logoutUser().unwrap();
    } catch (error) {
      console.error("Logout process failed:", error);
    }
    googleLogout();
    dispatch(api.util.resetApiState());
    handleMenuClose();
    navigate("/");
  };

  return (
    <AppBar
      position="fixed"
      sx={{
        height: 60,
        justifyContent: "center",
        zIndex: (theme) => theme.zIndex.drawer + 1,
      }}
    >
      <Toolbar sx={{ minHeight: 60, px: { xs: 1, sm: 2 } }}>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onToggleSidebar}
          sx={{ mr: { xs: 1, sm: 2 } }}
        >
          <MenuIcon />
        </IconButton>

        {/* ← Breadcrumb area */}
        <Box sx={{ flexGrow: 1, display: "flex", alignItems: "center" }}>
          <Breadcrumbs
            separator="›"
            aria-label="breadcrumb"
            sx={{ color: "inherit" }}
          >
            <Link
              component={RouterLink}
              to="/"
              underline="hover"
              color="inherit"
              sx={{ fontWeight: "bold" }}
            >
              TV LMS
            </Link>

            {courseMatch &&
              (courseLoading ? (
                <CircularProgress size={16} color="inherit" />
              ) : (
                <Typography color="inherit" sx={{ fontWeight: 500 }}>
                  {courseName}
                </Typography>
              ))}
          </Breadcrumbs>
        </Box>

        <Box sx={{ minWidth: 50 }}>
          {authLoading ? (
            <CircularProgress color="inherit" size={24} />
          ) : isAuthenticated ? (
            <IconButton color="inherit" onClick={handleMenuOpen} size="small">
              <Avatar sx={{ bgcolor: "secondary.main", width: 32, height: 32 }}>
                {user.name
                  ? user.name[0].toUpperCase()
                  : user.email
                  ? user.email[0].toUpperCase()
                  : "U"}
              </Avatar>
            </IconButton>
          ) : (
            <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID || ""}>
              <GoogleLogin
                onSuccess={handleGoogleLoginSuccess}
                onError={handleGoogleLoginError}
                useOneTap
                shape="rectangular"
                theme="outline"
                size="medium"
                width="auto"
                disabled={loginLoading}
              />
            </GoogleOAuthProvider>
          )}
        </Box>
      </Toolbar>

      {isAuthenticated && (
        <ProfileDropdown
          anchorEl={anchorEl}
          open={menuOpen}
          onClose={handleMenuClose}
          onLogout={handleLogout}
          userName={user.name || user.email}
        />
      )}
    </AppBar>
  );
}
