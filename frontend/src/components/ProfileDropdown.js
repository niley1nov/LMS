// src/components/ProfileDropdown.js
import React from 'react';

export default function ProfileDropdown({ onClose, onLogout }) {
  const menuStyle = {
    position: 'absolute',
    top: 'calc(100% + 8px)',
    right: 0,
    background: '#2a2a2a',
    borderRadius: '6px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.4)',
    minWidth: '140px',
    overflow: 'hidden',
    zIndex: 1001,
  };
  const itemStyle = {
    display: 'block',
    width: '100%',
    padding: '10px 16px',
    background: 'transparent',
    border: 'none',
    color: '#fff',
    textAlign: 'left',
    cursor: 'pointer',
    fontSize: '14px',
  };
  const arrowStyle = {
    position: 'absolute',
    top: '-6px',
    right: '12px',
    width: 0,
    height: 0,
    borderLeft: '6px solid transparent',
    borderRight: '6px solid transparent',
    borderBottom: '6px solid #2a2a2a',
  };

  return (
    <div style={menuStyle}>
      <div style={arrowStyle} />
      <button style={itemStyle} onClick={() => { onClose(); alert('Go to Profile'); }}>
        Profile
      </button>
      <button style={itemStyle} onClick={() => { onClose(); alert('Go to Settings'); }}>
        Settings
      </button>
      <hr style={{ margin: 0, borderColor: '#444' }} />
      <button style={itemStyle} onClick={() => { onLogout(); onClose(); }}>
        Logout
      </button>
    </div>
  );
}
