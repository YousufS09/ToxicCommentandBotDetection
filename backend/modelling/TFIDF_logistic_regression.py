import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import joblib
import os
import numpy as np

DATA_PATH = r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentandBotDetection\Data\Raw\FinalBalancedDataset.csv"
MODEL_DIR = r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentandBotDetection\Models\TFIDF"
os.makedirs(MODEL_DIR, exist_ok=True)
RANDOM_STATE = 42

def load_data(path):
    df = pd.read_csv(path)

    # rename columns from the toxic tweet dataset
    df = df.rename(columns={"tweet": "clean_tweet_final", "Toxicity": "label"})

    df = df.dropna(subset=["clean_tweet_final", "label"])
    df["clean_tweet_final"] = df["clean_tweet_final"].astype(str)
    df["label"] = df["label"].astype(int)

    print("Loaded:", df.shape)
    print("Label distribution:\n", df["label"].value_counts())
    return df

def train_and_save(df):
    X = df["clean_tweet_final"].values
    y = df["label"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english")
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    model = LogisticRegression(max_iter=2000, solver="liblinear", random_state=RANDOM_STATE)
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    y_proba = model.predict_proba(X_test_tfidf)[:, 1]

    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Fix → Avoid ROC AUC crash if only one class present
    if len(np.unique(y_test)) == 2:
        print("ROC AUC:", roc_auc_score(y_test, y_proba))
    else:
        print("ROC AUC: n/a (only one class present in y_test)")

    print(classification_report(y_test, y_pred))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

    joblib.dump(tfidf, os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))
    joblib.dump(model, os.path.join(MODEL_DIR, "tfidf_model.joblib"))

    from sklearn.pipeline import Pipeline
    pipe = Pipeline([("tfidf", tfidf), ("clf", model)])
    joblib.dump(pipe, os.path.join(MODEL_DIR, "tfidf_pipeline.joblib"))

    print("Saved vectorizer and model to:", MODEL_DIR)
    return pipe


if __name__ == "__main__":
    df = load_data(DATA_PATH)
    train_and_save(df)
