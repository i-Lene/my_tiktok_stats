import axios from "axios";

const api = axios.create({
  baseURL: "https://my-tiktok-stats.onrender.com",
});

export default api;
