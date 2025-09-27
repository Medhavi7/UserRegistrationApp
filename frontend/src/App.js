import React, { useState, useEffect } from "react";
import axios from "axios";
import ClientDashboard from "./components/ClientDashboard";
import AdminDashboard from "./components/AdminDashboard";

function App() {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(true); // Start with loading=true to check localStorage
  const [initializing, setInitializing] = useState(true);

  const backendUrl = process.env.REACT_APP_API_URL || "";

  // Check localStorage for existing token on app initialization
  useEffect(() => {
    const checkExistingAuth = async () => {
      console.log("🔍 Checking existing authentication...");
      const storedToken = localStorage.getItem("access_token");
      const storedRole = localStorage.getItem("user_role");
      
      console.log("📦 Stored token:", storedToken ? "Found" : "Not found");
      console.log("📦 Stored role:", storedRole);
      
      if (storedToken) {
        try {
          console.log("🔐 Verifying token with backend...");
          // Verify the token is still valid by making a request to /users/me
          const response = await axios.get(`${backendUrl}/users/me`, {
            headers: { Authorization: `Bearer ${storedToken}` }
          });
          
          console.log("✅ Token is valid! User data:", response.data);
          
          // Token is valid, set the state
          setToken(storedToken);
          setRole(storedRole || response.data.role);
          
          // Update stored role if it wasn't stored or is different
          if (!storedRole || storedRole !== response.data.role) {
            localStorage.setItem("user_role", response.data.role);
            setRole(response.data.role);
          }
          
          console.log("🎯 Auth state restored - token:", !!storedToken, "role:", storedRole || response.data.role);
        } catch (error) {
          // Token is invalid, clear localStorage
          console.error("❌ Token validation failed:", error.response?.data || error.message);
          console.log("🧹 Clearing localStorage...");
          localStorage.removeItem("access_token");
          localStorage.removeItem("user_role");
        }
      } else {
        console.log("🚪 No stored token found, showing login");
      }
      
      setInitializing(false);
      setLoading(false);
      console.log("🏁 Authentication check complete");
    };

    checkExistingAuth();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!username || !password || (isRegister && !email)) {
      alert("Please fill all required fields");
      return;
    }

    try {
      setLoading(true);
      let res;
      if (isRegister) {
        res = await axios.post(`${backendUrl}/register`, { username, email, password });
      } else {
        const data = new URLSearchParams();
        data.append("username", username);
        data.append("password", password);
        res = await axios.post(`${backendUrl}/login`, data, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });
      }

      if (!res.data.access_token) {
        throw new Error("No access token received");
      }

      console.log("🔑 Login successful! Response:", res.data);
      
      // Store token in localStorage and state
      localStorage.setItem("access_token", res.data.access_token);
      setToken(res.data.access_token);
      console.log("💾 Token stored in localStorage");

      // Use user info from login/register response
      let userRole;
      if (res.data.user) {
        userRole = res.data.user.role;
        console.log("👤 Role from login response:", userRole);
      } else {
        // Fallback to /users/me call for older API responses
        console.log("🔍 Fetching user role from /users/me...");
        const me = await axios.get(`${backendUrl}/users/me`, {
          headers: { Authorization: `Bearer ${res.data.access_token}` }
        });
        userRole = me.data.role;
        console.log("👤 Role from /users/me:", userRole);
      }
      
      // Store role in localStorage and state
      localStorage.setItem("user_role", userRole);
      setRole(userRole);
      console.log("💾 Role stored in localStorage:", userRole);

      // Clear form fields after successful login/register
      setUsername("");
      setEmail("");
      setPassword("");

    } catch (err) {
      console.error("Login/Register error:", err);
      const errorMessage = err.response?.data?.detail || err.message || "An error occurred";
      alert(`${isRegister ? "Registration" : "Login"} failed: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = `${backendUrl}/login/google`;
  };

  const handleLogout = () => {
    // Clear localStorage
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");
    
    // Clear state
    setToken("");
    setRole("");
    setUsername("");
    setEmail("");
    setPassword("");
  };

  // Show loading screen while checking authentication
  if (initializing) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="mb-4">Loading...</div>
        </div>
      </div>
    );
  }

  // If token exists, show the dashboard
  if (token) {
    if (!role || loading) {
      return (
        <div className="flex h-screen items-center justify-center bg-gray-100">
          <div className="text-center">
            <div className="mb-4">Loading dashboard...</div>
            <button
              onClick={handleLogout}
              className="text-blue-600 hover:underline"
            >
              Back to Login
            </button>
          </div>
        </div>
      );
    }
    return role === "admin" ? (
      <AdminDashboard token={token} onLogout={handleLogout} />
    ) : (
      <ClientDashboard token={token} onLogout={handleLogout} />
    );
  }

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <div className="bg-white shadow-lg rounded-2xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">
          {isRegister ? "Register" : "Login"} to GetCovered
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Username or Email"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
          />

          {isRegister && (
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
            />
          )}

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-gray-400"
          >
            {loading ? "Processing..." : (isRegister ? "Register" : "Login")}
          </button>
        </form>

        <div className="my-4 text-center text-gray-500">OR</div>

        <button
          onClick={handleGoogleLogin}
          className="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition flex items-center justify-center gap-2"
        >
          Sign in with Google
        </button>

        <p className="text-center mt-4 text-sm">
          {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            onClick={() => setIsRegister(!isRegister)}
            className="text-blue-600 hover:underline"
          >
            {isRegister ? "Login" : "Register"}
          </button>
        </p>
      </div>
    </div>
  );
}

export default App;
