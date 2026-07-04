import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: API_BASE_URL,
});


// Toxic Comment Detection API
export const predictToxic = (text) => {
  return API.post("/toxic/predict", { text }).then((response) => response.data);
};

// Bot Detection API
export const predictBot = (payload) => {
  return API.post("/bot/predict", payload).then((response) => response.data);
};

export default API;
