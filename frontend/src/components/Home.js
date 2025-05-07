// src/components/Home.js
import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const pageStyle = { textAlign: 'center', padding: '80px 20px' };

export default function Home() {
  const { protectedMessage } = useContext(AuthContext);

  return (
    <div style={pageStyle}>
      <h1>Welcome to the Learning Management System</h1>
      <p>Empower your team with interactive courses and quizzes.</p>
      <img src="/logo192.png" alt="LMS Logo" style={{ width: '150px', margin: '20px 0' }} />
      <p>Get started by signing up or logging in.</p>

      <div style={{ marginTop: '40px' }}>
        <h2>Protected Endpoint Response:</h2>
        <p>{protectedMessage}</p>
      </div>
    </div>
  );
}
