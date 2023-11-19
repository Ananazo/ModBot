// src/components/Dashboard.js
import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [status, setStatus] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/api/bot-status')
      .then(response => response.json())
      .then(data => setStatus(data.status));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Status: {status}</p>
    </div>
  );
};

export default Dashboard;