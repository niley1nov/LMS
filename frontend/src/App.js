// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Home from './components/Home';

// Layout constants
const NAVBAR_HEIGHT = 60;    // px

// Style objects
const styles = {
  routerWrapper: {
    margin: 0,
    padding: 0,
    boxSizing: 'border-box',
    fontFamily: 'Arial, sans-serif',
  },
  layout: {
    display: 'flex',
    position: 'relative',
    minHeight: `calc(100vh - ${NAVBAR_HEIGHT}px)`,
    marginTop: NAVBAR_HEIGHT,
  },
  backdrop: {
    position: 'fixed',
    top: NAVBAR_HEIGHT,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0, 0, 0, 0.5)',
    zIndex: 900,
  },
  main: {
    flex: 1,
    padding: '20px',
    overflowY: 'auto',
    background: '#fafafa',
  }
};

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div style={styles.routerWrapper}>
      <Router>
        <Navbar
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(o => !o)}
        />

        <Sidebar isOpen={sidebarOpen} />

        {sidebarOpen && <div style={styles.backdrop} onClick={() => setSidebarOpen(false)} />}

        <div style={styles.layout}>
          <main style={styles.main}>
            <Routes>
              <Route path="/" element={<Home />} />
            </Routes>
          </main>
        </div>
      </Router>
    </div>
  );
}
