import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const predictBot = async (payload) => {
  const response = await axios.post(
    `${API_BASE_URL}/bot/predict`,
    payload
  );
  return response.data;
};
