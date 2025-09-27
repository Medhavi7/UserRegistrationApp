import axios from "axios";
const API_URL = process.env.REACT_APP_API_URL || "https://getcovered-app12345-784ded765ea5.herokuapp.com/";
const api = axios.create({ baseURL: API_URL });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
export default api;