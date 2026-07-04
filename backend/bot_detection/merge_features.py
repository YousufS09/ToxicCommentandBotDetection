import pandas as pd

FEATURES_FILE = "Data/Processed/bot_features.csv"
EMBED_FILE = "Data/Processed/bio_embeddings.csv"
OUTPUT_FILE = "Data/Processed/bot_final_features.csv"

def main():
    df_feat = pd.read_csv(FEATURES_FILE)
    df_emb = pd.read_csv(EMBED_FILE)

    df = pd.merge(df_feat, df_emb, on="user_id", how="inner")

    df.to_csv(OUTPUT_FILE, index=False)
    print("Merged and saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
