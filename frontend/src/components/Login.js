// src/components/Login.js
import React from 'react';
import { GoogleLogin } from '@react-oauth/google';

const pageStyle = { textAlign: 'center', padding: '80px 20px' };
// Read API URL from env (with localhost fallback)
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Login = () => {
  const handleSuccess = ({ credential: idToken }) => {
    fetch(`${API_URL}/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',           // ⚡️ important: send/receive cookies
      body: JSON.stringify({ token: idToken }),
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        console.log('Logged in user:', data.user);
        // TODO: e.g. navigate to dashboard or update app state
      })
      .catch(err => console.error('Auth error:', err));
  };

  const handleError = () => {
    console.error('Google Login Failed');
  };

  return (
    <div style={pageStyle}>
      <h2>Login with Google</h2>
      <GoogleLogin onSuccess={handleSuccess} onError={handleError} />
    </div>
  );
};

export default Login;