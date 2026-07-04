import pandas as pd
import joblib
import os
from feature_engineering import feature_engineer

MODEL_PATH = "Models/Bot/bot_rf_model.joblib"

def load_model():
    return joblib.load(MODEL_PATH)

def predict_bot(df):
    model = load_model()
    fe_df = feature_engineer(df)
    X = fe_df.drop(columns=["label"])
    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]
    return preds, probs
