import pandas as pd
import numpy as np
import os

INPUT_PATH = "Data/Processed/bot_users_merged.csv"
OUTPUT_PATH = "Data/Processed/bot_users_features.csv"

def feature_engineer(df):
    df = df.copy()
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["account_age_days"] = (pd.Timestamp.now() - df["created_at"]).dt.days
    else:
        df["account_age_days"] = 0

    df["followers_count"] = pd.to_numeric(df.get("followers_count", 0), errors="coerce").fillna(0)
    df["friends_count"] = pd.to_numeric(df.get("friends_count", 0), errors="coerce").fillna(0)
    df["statuses_count"] = pd.to_numeric(df.get("statuses_count", 0), errors="coerce").fillna(0)

    df["follower_ratio"] = (df["followers_count"] + 1) / (df["friends_count"] + 1)
    df["tweets_per_day"] = df["statuses_count"] / (df["account_age_days"] + 1)

    df["bio_len"] = df["description"].fillna("").astype(str).apply(len) if "description" in df.columns else 0

    df["has_default_profile_image"] = df["default_profile_image"].astype(int) if "default_profile_image" in df.columns else 0

    df["verified_flag"] = df["verified"].astype(int) if "verified" in df.columns else 0

    features = [
        "followers_count",
        "friends_count",
        "statuses_count",
        "account_age_days",
        "follower_ratio",
        "tweets_per_day",
        "bio_len",
        "has_default_profile_image",
        "verified_flag",
    ]

    output = df[features]
    output["label"] = df["label"]

    return output

def main():
    df = pd.read_csv(INPUT_PATH)
    fe_df = feature_engineer(df)
    fe_df.to_csv(OUTPUT_PATH, index=False)
    print("Features saved to:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
