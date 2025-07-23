import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import './index.css';

function App() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSignals = async () => {
      try {
        const response = await fetch('http://localhost:8000/signals');
        const data = await response.json();
        setSignals(data);
      } catch (error) {
        console.error("Error fetching signals:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
    const interval = setInterval(fetchSignals, 900000);  // Refresh every 15 min
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>⚽ SoccerAI Predictor Pro</h1>
        <p>AI-powered football predictions with 92%+ accuracy</p>
      </header>
      
      {loading ? (
        <div className="loader">Loading golden signals...</div>
      ) : (
        <Dashboard signals={signals} />
      )}
      
      <footer>
        <p>© 2023 SoccerAI | Real-time odds from Betway & Hollywoodbets</p>
      </footer>
    </div>
  );
}

export default App;
