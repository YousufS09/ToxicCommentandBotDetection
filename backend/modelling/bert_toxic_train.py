import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TRANSFORMERS_NO_FLAX"] = "1"

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

DATA_PATH = r"Data/Processed/cyberbullying_binary.csv"
TEXT_COL = "clean_tweet_final"
LABEL_COL = "label"
MODEL_NAME = "bert-base-uncased"
OUTPUT_DIR = "Models/BERT_Toxic"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"🔹 Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=[TEXT_COL, LABEL_COL])
df[TEXT_COL] = df[TEXT_COL].astype(str)
df[LABEL_COL] = df[LABEL_COL].astype(int)

print("🔹 Data shape:", df.shape)
print("🔹 Label distribution:\n", df[LABEL_COL].value_counts())

train_df, valid_df = train_test_split(
    df,
    test_size=0.1,
    random_state=42,
    stratify=df[LABEL_COL]
)

print("🔹 Train size:", train_df.shape[0])
print("🔹 Valid size:", valid_df.shape[0])

train_ds = Dataset.from_pandas(train_df[[TEXT_COL, LABEL_COL]])
valid_ds = Dataset.from_pandas(valid_df[[TEXT_COL, LABEL_COL]])

train_ds = train_ds.rename_columns({TEXT_COL: "text", LABEL_COL: "labels"})
valid_ds = valid_ds.rename_columns({TEXT_COL: "text", LABEL_COL: "labels"})

print(f"🔹 Loading tokenizer: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_batch(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=128,
    )

print("🔹 Tokenizing train and validation sets...")
train_ds = train_ds.map(tokenize_batch, batched=True)
valid_ds = valid_ds.map(tokenize_batch, batched=True)

train_ds = train_ds.remove_columns(["text"])
valid_ds = valid_ds.remove_columns(["text"])

train_ds.set_format("torch")
valid_ds.set_format("torch")

print(f"🔹 Loading base model: {MODEL_NAME}")
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=2
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)

    acc = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        preds,
        average="binary"
    )

    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=2,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir=os.path.join(OUTPUT_DIR, "logs"),
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    logging_steps=50,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=valid_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

if __name__ == "__main__":
    print("🚀 Starting BERT fine-tuning for Toxic Comment Detection...")
    trainer.train()

    print("💾 Saving model and tokenizer to:", OUTPUT_DIR)
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("✅ Done! Fine-tuned BERT model saved in:", OUTPUT_DIR)
