import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Callback = () => {
  const location = useLocation();

  useEffect(() => {
    const fetchUserData = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');

      const response = await fetch(`http://localhost:5000/callback?code=${code}`);
      const data = await response.json();
      console.log(data); // Handle user data
    };

    fetchUserData();
  }, [location]);

  return (
    <div>
      <h1>Callback Page</h1>
      <p>Loading...</p>
    </div>
  );
};

export default Callback;