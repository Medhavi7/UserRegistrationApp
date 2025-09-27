import React, { useEffect, useState } from "react";
import api from "../api";

const UserProfile = ({ token, onLogout, onEditProfile }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;

    const fetchUserData = async () => {
      try {
        const res = await api.get("/users/me");
        setUser(res.data);
      } catch (err) {
        console.error(err);
        setError(err.response?.data?.detail || "Failed to fetch user info");
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [token]);

  const getInitials = () => {
    if (!user) return "U";
    const firstName = user.first_name || "";
    const lastName = user.last_name || "";
    const username = user.username || "";
    
    if (firstName && lastName) {
      return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
    } else if (firstName) {
      return firstName.charAt(0).toUpperCase();
    } else if (username) {
      return username.charAt(0).toUpperCase();
    }
    return "U";
  };

  const getDisplayName = () => {
    if (!user) return "User";
    const firstName = user.first_name || "";
    const lastName = user.last_name || "";
    
    if (firstName && lastName) {
      return `${firstName} ${lastName}`;
    } else if (firstName) {
      return firstName;
    } else if (user.username) {
      return user.username;
    }
    return "User";
  };

  const formatMemberSince = () => {
    if (!user?.created_at) return new Date().toLocaleDateString();
    return new Date(user.created_at).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">GetCovered</h1>
            <div className="flex items-center space-x-6">
              <span className="text-gray-600">Profile</span>
              <button
                onClick={onLogout}
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="text-center mb-12">
          {/* Avatar */}
          <div className="inline-flex items-center justify-center w-24 h-24 bg-blue-200 rounded-full mb-6">
            <span className="text-2xl font-semibold text-blue-800">
              {getInitials()}
            </span>
          </div>

          {/* Welcome Message */}
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Hello, {user?.username}!
          </h2>
          <p className="text-lg text-gray-600">
            Welcome to GetCovered. Your account has been successfully created.
          </p>
        </div>

        {/* Account Details Card */}
        <div className="bg-white rounded-lg shadow-sm border p-8 max-w-2xl mx-auto">
          <h3 className="text-xl font-semibold text-gray-900 mb-6 text-center">
            Account Details
          </h3>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600 font-medium">Name:</span>
              <span className="text-gray-900 font-medium">
                {getDisplayName()}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600 font-medium">Email:</span>
              <span className="text-gray-900 font-medium">
                {user?.email}
              </span>
            </div>
            
            <div className="flex justify-between items-center py-3">
              <span className="text-gray-600 font-medium">Member since:</span>
              <span className="text-gray-900 font-medium">
                {formatMemberSince()}
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center space-x-4 mt-8">
            <button
              onClick={onEditProfile}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Edit Profile
            </button>
            <button
              onClick={onLogout}
              className="bg-white text-gray-700 px-6 py-3 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors font-medium"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
