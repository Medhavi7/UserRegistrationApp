import React, {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import api from "../api";

const AuthCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // token passed as query param ?token=...
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    if (!token) {
      navigate("/unauthorized");
      return;
    }
    localStorage.setItem("access_token", token);
    // fetch profile
    api.get("/users/me").then(res => {
      const role = res.data.role;
      if (role === "admin") navigate("/admin");
      else navigate("/client");
    }).catch(err => {
      console.error(err);
      navigate("/unauthorized");
    });
  }, [navigate]);

  return <div>Processing login...</div>;
};

export default AuthCallback;