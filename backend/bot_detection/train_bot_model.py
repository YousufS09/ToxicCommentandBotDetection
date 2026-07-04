import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

FEATURES_PATH = "Data/Processed/bot_users_features.csv"
MODEL_DIR = "Models/Bot"
MODEL_PATH = os.path.join(MODEL_DIR, "bot_rf_model.joblib")

def main():
    df = pd.read_csv(FEATURES_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)

    print("Bot model saved at:", MODEL_PATH)

if __name__ == "__main__":
    main()
