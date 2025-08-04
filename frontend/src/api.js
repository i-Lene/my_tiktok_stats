import axios from "axios";

const api = axios.create({
  baseURL: "https://my-tiktok-stats-1.onrender.com",
});

export default api;
