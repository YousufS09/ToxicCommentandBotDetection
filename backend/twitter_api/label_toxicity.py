import pandas as pd
from detoxify import Detoxify

df = pd.read_csv(r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Data\Processed\clean_twitter_data.csv")

model = Detoxify('original')  

# Function to label tweets as Toxic or Non-Toxic
def label_toxicity(text, threshold=0.5):
    # Get toxicity score
    scores = model.predict(text)
    # scores['toxicity'] is a value between 0 and 1
    return 1 if scores['toxicity'] >= threshold else 0

# Apply labeling to your preprocessed tweets
df['label'] = df['clean_tweet_final'].apply(label_toxicity)

# Save the updated dataset
output_path = r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Data\Processed\clean_twitter_data_labeled.csv"
df.to_csv(output_path, index=False)

print("✅ Tweets labeled and saved to:", output_path)
print("\nSample of labeled tweets:\n")
print(df[['clean_tweet_final', 'label']].head(10))
