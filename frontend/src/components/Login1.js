import React from "react";
const Login = () => {
  const handleLogin = () => {
    // Redirect to backend OAuth start
    window.location.href = (process.env.REACT_APP_API_URL || "http://localhost:8000") + "/auth/login";
  };
  return (
    <div>
      <p>Sign in using your Google account (only @getcovered.io allowed)</p>
      <button onClick={handleLogin}>Sign in with Google</button>
    </div>
  );
};
export default Login;