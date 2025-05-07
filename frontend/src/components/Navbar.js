// src/components/Navbar.js
import React, { useContext, useState, useRef, useEffect } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { AuthContext } from '../context/AuthContext';
import ProfileDropdown from './ProfileDropdown';

const navStyle = {
  position: 'fixed', top: 0, left: 0, right: 0,
  background: '#333', padding: '10px 20px',
  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
  zIndex: 1000,
};
const linkStyle = {
  color: '#fff',
  textDecoration: 'none',
  fontWeight: 'bold',
  cursor: 'default'
};

export default function Navbar() {
  const { user, setUser, logout, refreshProtected } = useContext(AuthContext);
  console.log('Navbar render — user:', user);
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef();

  // Base URL for our API
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // click outside → close dropdown
  useEffect(() => {
    const handler = e => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('click', handler);
    return () => document.removeEventListener('click', handler);
  }, []);

  const handleSuccess = ({ credential }) => {
    console.log('🚀 Google SSO returned credential:', credential);
    fetch(`${API_URL}/auth/google`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: credential }),
    })
      .then(data => {
        console.log('⬅️ /auth/google payload:', data);
        if (!data.ok) throw new Error(`HTTP ${data.status}`);
        return data.json();
      })
      .then(data => {
        console.log('⬅️ /auth/google payload:', data);
        setUser(data.user);
        refreshProtected();
      })
      .catch(err => console.error('🚨 auth error:', err));
  };

  if (user === undefined) {
    return null;
  }

  return (
    <nav style={navStyle}>
      <div style={linkStyle}>Home</div>

      <div ref={wrapperRef} style={{ position: 'relative' }}>
        {!user ? (
          <GoogleLogin
            onSuccess={handleSuccess}
            onError={err => console.error('🚨 Google Login Failed:', err)}
          />

        ) : (
          <>
            <div
              onClick={() => setOpen(o => !o)}
              style={{
                width: '36px', height: '36px',
                borderRadius: '50%', background: '#555',
                color: '#fff', display: 'flex',
                alignItems: 'center', justifyContent: 'center',
                textTransform: 'uppercase', fontSize: '16px',
                userSelect: 'none', cursor: 'pointer'
              }}
            >
              {user.name[0]}
            </div>
            {open && (
              <ProfileDropdown
                onClose={() => setOpen(false)}
                onLogout={logout}
              />
            )}
          </>
        )}
      </div>
    </nav>
  );
}
