// src/components/Home.js
import React, { useEffect, useState } from 'react';

// Read API URL from env or default to localhost
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const pageStyle = { textAlign: 'center', padding: '80px 20px' };

const Home = () => {
  const [message, setMessage] = useState('Loading protected data...');

  useEffect(() => {
    fetch(`${API_URL}/protected`, {
      method: 'GET',
      credentials: 'include',
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => setMessage(data.message))
      .catch(err => {
        console.error('Protected fetch error:', err);
        setMessage('Not authenticated or error fetching data');
      });
  }, []);

  return (
    <div style={pageStyle}>
      <h1>Welcome to the Learning Management System</h1>
      <p>Empower your team with interactive courses and quizzes.</p>
      <img src="/logo192.png" alt="LMS Logo" style={{ width: '150px', margin: '20px 0' }} />
      <p>Get started by signing up or logging in.</p>

      <div style={{ marginTop: '40px' }}>
        <h2>Protected Endpoint Response:</h2>
        <p>{message}</p>
      </div>
    </div>
  );
};

export default Home;
