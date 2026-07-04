import tweepy
import pandas as pd
import os

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAO2n3wEAAAAAcwA4Gkm0teiyVMwko%2BuJctsuUuQ%3DAUXaMTT8BDC71rSk5ja5ETxYe4PWtlUaWUcsnEmI9x4dJRmBrZ"

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True
)

# Query for toxicity analysis
query = "Toxic OR Hate OR Harassment -is:retweet lang:en"

tweets = client.search_recent_tweets(
    query=query,
    max_results=10,
    expansions=["author_id"],       # needed to get user info
    tweet_fields=["created_at", "public_metrics", "lang"],
    user_fields=[
        "username", "name", "created_at", "description",
        "public_metrics", "profile_image_url"
    ],
)

# ---------------------------
# Extract User Dictionary
# ---------------------------
users = {u["id"]: u for u in tweets.includes["users"]}

records = []

for tweet in tweets.data:
    user = users.get(tweet.author_id, {})

    user_metrics = user["public_metrics"]

    row = {
        "tweet_id": tweet.id,
        "tweet_text": tweet.text,
        "tweet_created_at": tweet.created_at,
        "user_id": tweet.author_id,
        "user_name": user.get("name"),
        "username": user.get("username"),
        "bio": user.get("description", ""),
        "followers_count": user_metrics.get("followers_count", 0),
        "following_count": user_metrics.get("following_count", 0),
        "tweet_count": user_metrics.get("tweet_count", 0),
        "account_created_at": user.get("created_at"),
    }
    records.append(row)

df = pd.DataFrame(records)

os.makedirs("Data/Live", exist_ok=True)
file_path = "Data/Live/twitter_live_data.csv"
df.to_csv(file_path, index=False)

print(f"✅ Saved complete tweet & user info to {file_path}")
