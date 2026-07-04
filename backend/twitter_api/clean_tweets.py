import pandas as pd
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
import emoji

nltk.download('wordnet')
nltk.download('omw-1.4')

df = pd.read_csv(r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Data\Raw\twitter_data.csv")

def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\brt\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'@\w+', '', text)
    text = text.replace('#', '')
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = emoji.replace_emoji(text, replace='')
    text = text.translate(str.maketrans('', '', string.punctuation))
    text =                  text.lower().strip()
    return text

df['clean_tweet'] = df['tweet'].apply(clean_text)

lemmatizer = WordNetLemmatizer()

def lemmatize_text(text):
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

df['clean_tweet_final'] = df['clean_tweet'].apply(lemmatize_text)

output_path = r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Data\Processed\clean_twitter_data.csv"
df.to_csv(output_path, index=False)

print("\n✅ Cleaned and fully processed tweets saved to Data/Processed/clean_twitter_data.csv")
print("\nSample of cleaned tweets:\n")
print(df['clean_tweet_final'].head(10))
