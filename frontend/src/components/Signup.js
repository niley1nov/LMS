// src/components/Signup.js
import React from 'react';
import { GoogleLogin } from '@react-oauth/google';

const pageStyle = { textAlign: 'center', padding: '80px 20px' };
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Signup = () => {
  const handleSuccess = ({ credential: idToken }) => {
    fetch(`${API_URL}/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ token: idToken }),
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        console.log('Signed up user:', data.user);
        // redirect or update your UI
      })
      .catch(err => console.error('Signup error:', err));
  };

  const handleError = () => console.error('Google Signup Failed');

  return (
    <div style={pageStyle}>
      <h2>Signup with Google</h2>
      <GoogleLogin onSuccess={handleSuccess} onError={handleError} />
    </div>
  );
};

export default Signup;