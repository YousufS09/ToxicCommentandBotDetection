import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

export const analyzeCombined = async ({
  comment,
  description,
  followers_count,
  following_count,
  tweet_count,
  account_age_days,
}) => {
  const response = await axios.post(`${API_BASE_URL}/analysis/combined`, {
    comment,
    description,
    followers_count: Number(followers_count),
    following_count: Number(following_count),
    tweet_count: Number(tweet_count),
    account_age_days: Number(account_age_days),
  });

  return response.data;
};
