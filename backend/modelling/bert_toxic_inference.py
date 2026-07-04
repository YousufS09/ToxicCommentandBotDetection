import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = "Models/BERT_Toxic"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.to(device)
model.eval()

LABEL_MAP = {
    0: "non_toxic",
    1: "toxic"
}

@torch.no_grad()
def predict_toxicity(texts):
    if isinstance(texts, str):
        texts = [texts]

    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )

    input_ids = encodings["input_ids"].to(device)
    attention_mask = encodings["attention_mask"].to(device)

    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=-1)

    scores, preds = torch.max(probs, dim=-1)

    results = []
    for text, pred, score in zip(texts, preds, scores):
        label_id = pred.item()
        label_name = LABEL_MAP[label_id]
        results.append({
            "text": text,
            "label_id": label_id,
            "label": label_name,
            "confidence": float(score.item())
        })

    return results

if __name__ == "__main__":
    samples = [
        "I hate you so much, you're useless.",
        "Thanks for your help, really appreciate it!"
    ]
    outputs = predict_toxicity(samples)
    for out in outputs:
        print(f"Text: {out['text']}")
        print(f"Prediction: {out['label']} (confidence={out['confidence']:.4f})")
        print("-" * 50)
