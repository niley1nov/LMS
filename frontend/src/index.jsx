// src/index.js
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App"; // Your main application component
import { GoogleOAuthProvider } from "@react-oauth/google";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

// 1. Import the Redux Provider and your store
import { Provider as ReduxProvider } from 'react-redux';
import { store } from './redux/store'; // Assuming your store is exported from src/redux/store.js

// Create a custom Material UI theme (this part remains the same)
const theme = createTheme({
  palette: {
    primary: { main: "#1976d2" }, // Example primary color
    secondary: { main: "#9c27b0" }, // Example secondary color
    // You can customize other palette options like background, error, warning, etc.
  },
  typography: {
    fontFamily: "Roboto, sans-serif", // Default font
    // You can customize variants like h1, h2, body1, etc.
  },
  // You can also customize components, spacing, breakpoints, etc.
  // components: {
  //   MuiButton: {
  //     styleOverrides: {
  //       root: {
  //         borderRadius: 8,
  //       },
  //     },
  //   },
  // },
});

// Ensure your Google Client ID is available
const googleClientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;
if (!googleClientId) {
  console.error("ERROR: REACT_APP_GOOGLE_CLIENT_ID is not defined in your .env file. Google Authentication will not work.");
  // Optionally, you could render an error message to the DOM here
  // or prevent the app from rendering fully.
}

const root = createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Applies baseline Material UI styles */}
      {/* 2. Wrap the App with GoogleOAuthProvider (if client ID exists) and ReduxProvider */}
      {googleClientId ? (
        <GoogleOAuthProvider clientId={googleClientId}>
          <ReduxProvider store={store}>
            <App />
          </ReduxProvider>
        </GoogleOAuthProvider>
      ) : (
        // Render a fallback or error message if Google Client ID is missing
        <div>
          <h1>Configuration Error</h1>
          <p>Google Client ID is missing. Please check your environment variables.</p>
          <p>Google Authentication will not be available.</p>
          {/* You might still want to render the app without Google Auth
              or a more specific error page. For now, showing an error.
              If you still want the app to run without Google Auth,
              you'd structure this differently.
          */}
          <ReduxProvider store={store}>
            <App />
          </ReduxProvider>
        </div>
      )}
    </ThemeProvider>
  </React.StrictMode>
);