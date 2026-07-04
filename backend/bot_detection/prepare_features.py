import pandas as pd
import os
from datetime import datetime

INPUT_FILE = "Data/Processed/bot_merged.csv"
OUTPUT_FILE = "Data/Processed/bot_features.csv"

def load_data():
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    # Possible user id column names
    user_cols = ["user_id", "userid", "id", "user", "profile_id"]
    for col in user_cols:
        if col in df.columns:
            df = df.rename(columns={col: "user_id"})
            break

    if "user_id" not in df.columns:
        raise ValueError("ERROR: No user_id column found in bot_merged.csv")

    # Auto-fix text column
    text_cols = ["text", "tweet_text", "content", "status", "tweet"]
    for col in text_cols:
        if col in df.columns:
            df = df.rename(columns={col: "text"})
            break
    if "text" not in df.columns:
        df["text"] = ""

    # Auto-fix numeric columns
    rename_map = {
        "followers": "followers_count",
        "friends": "following_count",
        "following": "following_count",
        "statuses_count": "tweet_count",
    }
    df = df.rename(columns=rename_map)

    for col in ["followers_count", "following_count", "tweet_count"]:
        if col not in df.columns:
            df[col] = 0

    return df


def compute_features(df):
    # Handle timestamps safely
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        try:
            df["created_at"] = df["created_at"].dt.tz_localize(None)
        except:
            pass
        df["account_age_days"] = (datetime.now() - df["created_at"]).dt.days
    else:
        df["account_age_days"] = 0

    df["followers_count"] = df["followers_count"].fillna(0)
    df["following_count"] = df["following_count"].fillna(0)
    df["tweet_count"] = df["tweet_count"].fillna(0)

    df["follow_ratio"] = df["followers_count"] / (df["following_count"] + 1)

    df["tweet_length"] = df["text"].astype(str).apply(len)
    df["hashtags"] = df["text"].astype(str).apply(lambda x: x.count("#"))
    df["mentions"] = df["text"].astype(str).apply(lambda x: x.count("@"))

    # Ensure label exists; if not, set 0 for all
    if "label" not in df.columns:
        df["label"] = 0

    features = df.groupby("user_id").agg({
        "followers_count": "max",
        "following_count": "max",
        "tweet_count": "max",
        "account_age_days": "max",
        "follow_ratio": "max",
        "tweet_length": "mean",
        "hashtags": "mean",
        "mentions": "mean",
        "label": "max"
    }).reset_index()

    return features


def save_features(df):
    os.makedirs("Data/Processed", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Saved features to: {OUTPUT_FILE}\n")


def main():
    df = load_data()
    features = compute_features(df)
    save_features(features)


if __name__ == "__main__":
    main()
