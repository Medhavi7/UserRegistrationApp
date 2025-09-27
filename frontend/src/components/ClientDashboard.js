// src/ClientDashboard.js
import React, { useState } from "react";
import UserProfile from "./UserProfile";
import EditProfile from "./EditProfile";

const ClientDashboard = ({ token, onLogout }) => {
  const [currentView, setCurrentView] = useState("profile"); // "profile" or "edit"

  const handleEditProfile = () => {
    setCurrentView("edit");
  };

  const handleBackToProfile = () => {
    setCurrentView("profile");
  };

  if (currentView === "edit") {
    return (
      <EditProfile 
        token={token} 
        onLogout={onLogout} 
        onBackToProfile={handleBackToProfile}
      />
    );
  }

  return (
    <UserProfile 
      token={token} 
      onLogout={onLogout} 
      onEditProfile={handleEditProfile}
    />
  );
};

export default ClientDashboard;
