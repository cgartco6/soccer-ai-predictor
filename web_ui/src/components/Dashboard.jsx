import React from 'react';
import SignalCard from './SignalCard';

const Dashboard = ({ signals }) => {
  return (
    <div className="dashboard">
      <div className="stats-bar">
        <div className="stat">
          <h3>{signals.length}</h3>
          <p>Golden Signals</p>
        </div>
        <div className="stat">
          <h3>92.7%</h3>
          <p>Avg Accuracy</p>
        </div>
        <div className="stat">
          <h3>22.3%</h3>
          <p>Avg Value Edge</p>
        </div>
      </div>
      
      <div className="signals-grid">
        {signals.length > 0 ? (
          signals.map((signal, index) => (
            <SignalCard key={index} signal={signal} />
          ))
        ) : (
          <div className="no-signals">
            <p>No golden signals found. Next scan in 15 minutes...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
