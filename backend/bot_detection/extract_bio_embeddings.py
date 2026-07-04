import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os

INPUT_FILE = "Data/Processed/bot_merged.csv"
OUTPUT_FILE = "Data/Processed/bio_embeddings.csv"

def load_data():
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    df = df[["id", "description", "label"]]
    df = df.rename(columns={"id": "user_id"})
    df["description"] = df["description"].fillna("")
    return df

def compute_embeddings(text_list):
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    embeddings = model.encode(text_list, batch_size=32, show_progress_bar=True)
    return embeddings

def main():
    df = load_data()
    embeddings = compute_embeddings(df["description"].tolist())
    emb_cols = [f"embed_{i}" for i in range(embeddings.shape[1])]
    emb_df = pd.DataFrame(embeddings, columns=emb_cols)
    emb_df["user_id"] = df["user_id"].values
    emb_df["label"] = df["label"].values
    os.makedirs("Data/Processed", exist_ok=True)
    emb_df.to_csv(OUTPUT_FILE, index=False)
    print("Saved:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
