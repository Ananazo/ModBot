import React from 'react';

const Login = () => {
  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/login'; // Adjust the URL to match your backend
  };

  return (
    <div>
      <h1>Login Page</h1>
      <button onClick={handleLogin}>Login with Discord</button>
    </div>
  );
};

export default Login;