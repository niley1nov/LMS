// src/components/Home.js
import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const sectionStyle = { marginBottom: '40px', paddingTop: '20px', };

export default function Home() {
  const { protectedMessage } = useContext(AuthContext);

  return (
    <div>
      <section id="overview" style={sectionStyle}>
        <h2>Course Overview</h2>
        <p>Welcome to your personalized learning journey. This course will guide you through …</p>
      </section>

      <section id="modules" style={sectionStyle}>
        <h2>Modules</h2>
        <ul>
          <li>Module 1: Getting Started</li>
          <li>Module 2: Intermediate Concepts</li>
          <li>Module 3: Advanced Techniques</li>
        </ul>
      </section>

      <section id="quizzes" style={sectionStyle}>
        <h2>Quizzes</h2>
        <p>Test your knowledge with periodic quizzes after each module.</p>
      </section>

      <section id="resources" style={sectionStyle}>
        <h2>Resources</h2>
        <p>Downloadable materials, slides, and reference guides.</p>
      </section>

      <section id="help" style={sectionStyle}>
        <h2>Help & Support</h2>
        <p>If you run into any issues, reach out to our support team at support@example.com.</p>
      </section>

      <section>
        <h2>Your Access Status</h2>
        <p>{protectedMessage}</p>
      </section>
    </div>
  );
}
