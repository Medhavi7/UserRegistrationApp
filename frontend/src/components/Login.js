import React, { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const toggleForm = () => setIsRegister(!isRegister);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!username || (!password || (isRegister && !email))) {
      alert("Please fill all required fields");
      return;
    }

    const url = isRegister
      ? `${API_URL}/register`
      : `${API_URL}/login`;

    const body = isRegister
      ? JSON.stringify({ username, email, password })
      : new URLSearchParams({ username, password }).toString();

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: isRegister
          ? { "Content-Type": "application/json" }
          : { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });

      let data;
      try {
        data = await res.json();
      } catch (jsonErr) {
        console.error("Invalid JSON response:", jsonErr);
        alert("Error: Invalid response from server");
        return;
      }

      console.log("Backend response:", data, res.status);

      if (res.ok) {
        alert("Success! Token: " + (data.access_token || "No token returned"));
      } else {
        // Show detailed backend error if available
        alert(
          `Error: ${
            data.detail || data.message || JSON.stringify(data) || "Unknown error"
          }`
        );
      }
    } catch (err) {
      console.error("Network error:", err);
      alert(`Network error: ${err.message}`);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const res = await fetch(`${API_URL}/login/google`, {
        method: "GET",
        redirect: "manual", // prevent automatic redirect
      });

      if (res.status >= 300 && res.status < 400) {
        const redirectUrl = res.headers.get("Location");
        if (redirectUrl) {
          window.location.href = redirectUrl;
        } else {
          alert("Redirect failed: no Location header");
        }
      } else {
        let data;
        try {
          data = await res.json();
        } catch {
          data = null;
        }
        alert(
          `Google login failed: ${data?.detail || "Unknown error, check backend logs"}`
        );
      }
    } catch (err) {
      console.error("Network error during Google login:", err);
      alert(`Network error: ${err.message}`);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="bg-white shadow-xl rounded-xl p-10 w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">
          {isRegister ? "Register" : "Login"}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
          />
          {isRegister && (
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            />
          )}
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-lg"
          >
            {isRegister ? "Register" : "Login"}
          </button>
        </form>

        <div className="text-center my-4 text-gray-500">OR</div>

        <button
          onClick={handleGoogleLogin}
          className="w-full flex items-center justify-center gap-2 border py-2 rounded-lg"
        >
          <img
            src="https://www.svgrepo.com/show/355037/google.svg"
            alt="Google"
            className="w-5 h-5"
          />
          Sign in with Google
        </button>

        <div className="mt-4 text-center">
          <button
            onClick={toggleForm}
            className="text-blue-600 hover:underline"
          >
            {isRegister
              ? "Already have an account? Login"
              : "New here? Register"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
