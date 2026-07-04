import os
import pandas as pd

RAW_PATH = r"Data/Raw/cyberbullying_tweets.csv"
OUT_PATH = r"Data/Processed/cyberbullying_binary.csv"

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

df = pd.read_csv(RAW_PATH)

df["label"] = (df["cyberbullying_type"] != "not_cyberbullying").astype(int)
df = df.rename(columns={"tweet_text": "clean_tweet_final"})
df = df[["clean_tweet_final", "label"]]

df.to_csv(OUT_PATH, index=False)

print("Columns:", df.columns.tolist())
print(df.head())
print("Label distribution:")
print(df["label"].value_counts())
print("Saved processed file to:", OUT_PATH)
