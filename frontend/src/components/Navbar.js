// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const navStyle = {
  position: 'fixed', top: 0, left: 0, right: 0,
  background: '#333', padding: '10px', display: 'flex', justifyContent: 'center'
};
const linkStyle = { color: '#fff', margin: '0 15px', textDecoration: 'none', fontWeight: 'bold' };

const Navbar = () => (
  <nav style={navStyle}>
    <Link to="/" style={linkStyle}>Home</Link>
    <Link to="/login" style={linkStyle}>Login</Link>
    <Link to="/signup" style={linkStyle}>Signup</Link>
  </nav>
);

export default Navbar;