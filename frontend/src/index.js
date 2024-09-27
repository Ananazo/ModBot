import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Home from './sites/home';
import Login from './sites/login';
import Callback from './sites/callback';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Router>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<Home />} />
      <Route path="/callback" element={<Callback />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  </Router>
);