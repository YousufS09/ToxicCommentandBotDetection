from functools import lru_cache
from pathlib import Path
import datetime
import json

import joblib
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer


BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_DIR / "Models"
TOXIC_MODEL_DIR = MODELS_DIR / "BERT_Toxic"
BOT_MODEL_PATH = MODELS_DIR / "bot_hybrid_rf.pkl"
BOT_FEATURE_INFO_PATH = MODELS_DIR / "bot_feature_info.json"
SBERT_MODEL_DIR = MODELS_DIR / "sbert_encoder"


def _extract_checkpoint_step(path: Path) -> int:
    try:
        return int(path.name.split("-")[-1])
    except (ValueError, IndexError):
        return -1


def _resolve_toxic_model_dir() -> Path:
    checkpoints = sorted(
        [path for path in TOXIC_MODEL_DIR.glob("checkpoint-*") if path.is_dir()],
        key=_extract_checkpoint_step,
    )
    return checkpoints[-1] if checkpoints else TOXIC_MODEL_DIR


@lru_cache(maxsize=1)
def get_toxic_assets():
    model_dir = _resolve_toxic_model_dir()
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        str(model_dir), local_files_only=True
    )
    model.eval()
    return tokenizer, model


@lru_cache(maxsize=1)
def get_bot_model():
    return joblib.load(BOT_MODEL_PATH)


@lru_cache(maxsize=1)
def get_bot_feature_names():
    with open(BOT_FEATURE_INFO_PATH, "r", encoding="utf-8") as file:
        return json.load(file)["feature_names"]


@lru_cache(maxsize=1)
def get_bot_encoder():
    return SentenceTransformer(str(SBERT_MODEL_DIR))


def _interpret_binary_result(label: str, confidence: float, positive_label: str) -> str:
    if label == positive_label:
        if confidence >= 0.8:
            return f"Strong {positive_label.lower()} signal"
        if confidence >= 0.6:
            return f"Moderate {positive_label.lower()} signal"
        return f"Possible {positive_label.lower()} signal"

    if confidence >= 0.8:
        return f"Strongly {positive_label.lower()}-free signal"
    if confidence >= 0.6:
        return f"Mostly {positive_label.lower()}-free signal"
    return f"Low {positive_label.lower()} signal"


def predict_toxic_text(text: str):
    tokenizer, model = get_toxic_assets()
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

    confidence, label_id = torch.max(probs, dim=1)
    label = "Toxic" if label_id.item() == 1 else "Non-Toxic"
    confidence_value = round(confidence.item(), 4)

    return {
        "label": label,
        "confidence": confidence_value,
        "interpretation": _interpret_binary_result(label, confidence_value, "Toxic"),
    }


def _resolve_account_age_days(user) -> int:
    if getattr(user, "account_age_days", None) is not None:
        return int(user.account_age_days)

    created_at = pd.to_datetime(getattr(user, "created_at", None), errors="coerce")
    if pd.notnull(created_at):
        return max((datetime.datetime.now() - created_at).days, 0)
    return 0


def extract_bot_features(user):
    feature_names = get_bot_feature_names()
    sbert = get_bot_encoder()
    account_age_days = _resolve_account_age_days(user)
    followers = int(getattr(user, "followers_count", 0))
    following = int(getattr(user, "following_count", 0))
    bio = getattr(user, "description", "") or ""
    embedding = sbert.encode([bio])[0]

    features = {
        "followers_count": followers,
        "following_count": following,
        "tweet_count": int(getattr(user, "tweet_count", 0)),
        "account_age_days": account_age_days,
        "follow_ratio": followers / (following + 1),
        "tweet_length": len(bio),
        "hashtags": bio.count("#"),
        "mentions": bio.count("@"),
    }

    for i, value in enumerate(embedding):
        features[f"emb_{i}"] = value

    df = pd.DataFrame([features])
    return df.reindex(columns=feature_names, fill_value=0)


def predict_bot_user(user):
    model = get_bot_model()
    X = extract_bot_features(user)
    prediction = model.predict(X)[0]

    if hasattr(model, "predict_proba"):
        positive_index = 1
        if hasattr(model, "classes_") and 1 in list(model.classes_):
            positive_index = list(model.classes_).index(1)
        confidence = float(model.predict_proba(X)[0][positive_index])
    else:
        confidence = 0.5

    confidence_value = round(confidence, 4)
    label = "Bot" if prediction == 1 else "Human"

    return {
        "prediction": label,
        "confidence": confidence_value,
        "interpretation": _interpret_binary_result(label, confidence_value, "Bot"),
        "account_age_days": _resolve_account_age_days(user),
    }


def analyze_combined_payload(payload):
    toxic = predict_toxic_text(payload.comment)
    bot = predict_bot_user(payload)

    toxicity_risk = toxic["confidence"] if toxic["label"] == "Toxic" else 1 - toxic["confidence"]
    bot_risk = bot["confidence"] if bot["prediction"] == "Bot" else 1 - bot["confidence"]
    risk_score = round((toxicity_risk + bot_risk) / 2, 4)

    if risk_score >= 0.75:
        risk_level = "High Risk"
        recommendation = "Review this account and comment urgently."
        summary = "The account and comment both show strong risk indicators."
    elif risk_score >= 0.45:
        risk_level = "Medium Risk"
        recommendation = "Review manually before taking action."
        summary = "There are mixed signals and the output should be reviewed."
    else:
        risk_level = "Low Risk"
        recommendation = "No immediate action is required."
        summary = "The account and comment currently look low risk."

    return {
        "toxic": toxic,
        "bot": bot,
        "toxicity_risk": toxicity_risk,
        "bot_risk": bot_risk,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "summary": summary,
        "recommendation": recommendation,
    }
