import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, classification_report
import joblib

FEATURE_FILE = "Data/Processed/bot_features.csv"
MODEL_DIR = "Models/"
os.makedirs(MODEL_DIR, exist_ok=True)

ENCODER_PATH = os.path.join(MODEL_DIR, "sbert_encoder")
SCALER_PATH = os.path.join(MODEL_DIR, "feature_scaler.pkl")
MODEL_PATH = os.path.join(MODEL_DIR, "rf_classifier.pkl")

def load_features():
    df = pd.read_csv(FEATURE_FILE, low_memory=False)
    if "description" not in df.columns:
        df["description"] = ""
    df["description"] = df["description"].fillna("")
    y = df["label"]
    numeric_df = df.drop(columns=["label", "description", "user_id"], errors="ignore")
    X_numeric = numeric_df.values
    text_list = df["description"].tolist()
    return X_numeric, text_list, y

def encode_text(text_list):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(text_list, batch_size=32, show_progress_bar=True)
    model.save(ENCODER_PATH)
    return embeddings, model

def train_model(X_numeric, X_text, y):
    scaler = StandardScaler()
    X_numeric_scaled = scaler.fit_transform(X_numeric)
    X_combined = np.hstack([X_numeric_scaled, X_text])
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y, test_size=0.2, random_state=42
    )
    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(clf, MODEL_PATH)

def main():
    X_numeric, text_list, y = load_features()
    X_text, _ = encode_text(text_list)
    train_model(X_numeric, X_text, y)

if __name__ == "__main__":
    main()
