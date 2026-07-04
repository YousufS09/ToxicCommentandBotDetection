import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
import os
import json

DATA_FILE = "Data/Processed/bot_final_features.csv"
MODEL_DIR = "Models"
MODEL_FILE = f"{MODEL_DIR}/bot_hybrid_rf.pkl"
FEATURE_INFO_FILE = f"{MODEL_DIR}/bot_feature_info.json"

def main():
    df = pd.read_csv(DATA_FILE)

    if "user_id" not in df.columns and "id" in df.columns:
        df = df.rename(columns={"id": "user_id"})

    X = df.drop(["label_y", "user_id"], axis=1, errors="ignore")
    y = df["label_y"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    feature_info = {
        "feature_names": list(X.columns)
    }
    with open(FEATURE_INFO_FILE, "w") as f:
        json.dump(feature_info, f)

    print("Saved model to:", MODEL_FILE)
    print("Saved feature info to:", FEATURE_INFO_FILE)

if __name__ == "__main__":
    main()
