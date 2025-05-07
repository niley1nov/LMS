// src/components/Sidebar.js
import React from 'react';

export default function Sidebar({ isOpen }) {
  const sidebarStyle = {
    position: 'fixed',
    top: '60px',
    left: 0,
    bottom: 0,
    width: '200px',
    background: '#f5f5f5',
    padding: '20px',
    boxShadow: '2px 0 5px rgba(0,0,0,0.1)',
    transform: isOpen ? 'translateX(0)' : 'translateX(-100%)',
    transition: 'transform 0.3s ease',
    zIndex: 1000,      // above the backdrop
    overflowY: 'auto'
  };

  const linkStyle = {
    display: 'block',
    margin: '10px 0',
    color: '#333',
    textDecoration: 'none',
    fontWeight: '500'
  };

  return (
    <nav style={sidebarStyle}>
      <h3>Course Navigation</h3>
      <a href="#overview" style={linkStyle}>Overview</a>
      <a href="#modules" style={linkStyle}>Modules</a>
      <a href="#quizzes" style={linkStyle}>Quizzes</a>
      <a href="#resources" style={linkStyle}>Resources</a>
      <a href="#help" style={linkStyle}>Help & Support</a>
    </nav>
  );
}
