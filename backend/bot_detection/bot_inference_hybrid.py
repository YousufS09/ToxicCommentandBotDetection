import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import joblib
import json
import datetime

MODEL_PATH = "Models/bot_hybrid_rf.pkl"
FEATURE_INFO_PATH = "Models/bot_feature_info.json"

SBERT_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
sbert = SentenceTransformer(SBERT_MODEL_NAME)

model = joblib.load(MODEL_PATH)

with open(FEATURE_INFO_PATH, "r") as f:
    feature_info = json.load(f)
feature_names = feature_info["feature_names"]

def extract_numeric_features(user):
    created_at = pd.to_datetime(user.get("created_at"), errors="coerce")
    account_age_days = (datetime.datetime.now() - created_at).days if created_at is not None else 0

    followers = user.get("followers_count", 0)
    following = user.get("following_count", 0)
    tweet_count = user.get("tweet_count", 0)

    follow_ratio = followers / (following + 1)

    bio = user.get("description", "")
    hashtags = bio.count("#")
    mentions = bio.count("@")
    tweet_length = len(bio)

    return {
        "followers_count": followers,
        "following_count": following,
        "tweet_count": tweet_count,
        "account_age_days": account_age_days,
        "follow_ratio": follow_ratio,
        "tweet_length": tweet_length,
        "hashtags": hashtags,
        "mentions": mentions,
    }

def predict_user(user):
    numeric_features = extract_numeric_features(user)

    embedding = sbert.encode([user.get("description", "")])[0]

    full_feature_vector = {**numeric_features}

    for i, val in enumerate(embedding):
        full_feature_vector[f"emb_{i}"] = val

    df = pd.DataFrame([full_feature_vector])

    df = df.reindex(columns=feature_names, fill_value=0)

    pred = model.predict(df)[0]

    return "Bot" if pred == 1 else "Human"

if __name__ == "__main__":
    sample_user = {
        "description": "Tech enthusiast. Love coding and AI!",
        "followers_count": 120,
        "following_count": 95,
        "tweet_count": 300,
        "created_at": "2018-06-20"
    }

    print("Prediction:", predict_user(sample_user))
