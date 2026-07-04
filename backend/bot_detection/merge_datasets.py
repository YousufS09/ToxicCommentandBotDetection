import os
import pandas as pd

BASE = "Data/Raw/Bot"
BOTS = os.path.join(BASE, "BotDatasets")
GENUINE = os.path.join(BASE, "GenuineDataset")

def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf-8", low_memory=False)
    except:
        return pd.read_csv(path, encoding="latin-1", low_memory=False)

def load_folder(folder_path, label):
    users = os.path.join(folder_path, "users.csv")
    tweets = os.path.join(folder_path, "tweets.csv")

    if not os.path.exists(users):
        return None

    df_users = read_csv_safe(users)
    if os.path.exists(tweets):
        df_tweets = read_csv_safe(tweets)
        if "user_id" in df_users.columns and "user_id" in df_tweets.columns:
            df = pd.merge(df_users, df_tweets, on="user_id", how="left")
        else:
            df = df_users.copy()
    else:
        df = df_users.copy()

    df["label"] = label
    return df

def merge_all():
    all_data = []

    print("\n===== Processing BOT folders =====\n")

    for folder in os.listdir(BOTS):
        folder_path = os.path.join(BOTS, folder)
        if os.path.isdir(folder_path):
            print(f"Processing: {folder}")
            df = load_folder(folder_path, 1)
            if df is not None:
                all_data.append(df)

    print("\n===== Adding Genuine Users =====\n")

    df_genuine = load_folder(GENUINE, 0)
    if df_genuine is not None:
        all_data.append(df_genuine)

    final = pd.concat(all_data, ignore_index=True)
    out_path = "Data/Processed/bot_merged.csv"
    os.makedirs("Data/Processed", exist_ok=True)
    final.to_csv(out_path, index=False)

    print(f"\n✅ Finished! Saved merged dataset to: {out_path}\n")

merge_all()
