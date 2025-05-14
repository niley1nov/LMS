// src/index.jsx
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { theme } from "./theme";
import { Provider as ReduxProvider } from 'react-redux';
import { store } from './redux/store';

const googleClientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;
if (!googleClientId) {
  console.error("ERROR: REACT_APP_GOOGLE_CLIENT_ID is not defined in your .env file. Google Authentication will not work.");
}

const root = createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {!googleClientId && (
        <div className="config-error">
          <h1>Configuration Error</h1>
          <p>Missing REACT_APP_GOOGLE_CLIENT_ID.</p>
        </div>
      )}
      <GoogleOAuthProvider clientId={googleClientId || ""}>
        <ReduxProvider store={store}>
          <App />
        </ReduxProvider>
      </GoogleOAuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);