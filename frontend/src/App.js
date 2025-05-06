import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("Loading...");

  // Read the API URL from env or default to localhost
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  useEffect(() => {
    fetch(API_URL)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((data) => setMessage(data.message))
      .catch((err) => {
        console.error("Fetch error:", err);
        setMessage("API error");
      });
  }, [API_URL]);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>LMS Frontend</h1>
      <p>Backend says: {message}</p>
    </div>
  );
}

export default App;
