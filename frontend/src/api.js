import axios from 'axios';

const baseURL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8001'                      // local backend for dev
  : 'https://my-tiktok-stats.onrender.com';     // your Render backend URL in prod

const api = axios.create({
  baseURL,
});

export default api;
