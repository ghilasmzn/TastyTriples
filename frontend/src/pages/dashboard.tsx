import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1>Welcome to the Dashboard!</h1>
      <button
        onClick={() => {
          localStorage.removeItem('isLoggedIn');
          window.location.reload();
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default Dashboard;
