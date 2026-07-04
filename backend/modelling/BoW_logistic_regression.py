# 1️⃣ Import required libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

# 2️⃣ Load the labeled dataset
data_path = r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Data\Processed\clean_twitter_data_labeled.csv"
df = pd.read_csv(data_path)

print("✅ Data loaded successfully!")
print(df.head())

# 3️⃣ Split data into train and test sets
X = df['clean_tweet_final']    # Input text
y = df['label']                # Toxicity label (0 or 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("✅ Data split into training and testing sets.")

# 4️⃣ Convert text into numerical features using Bag of Words
vectorizer = CountVectorizer(max_features=5000, stop_words='english')
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)

print("✅ Text converted into Bag of Words features.")

# 5️⃣ Train Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_bow, y_train)

print("✅ Logistic Regression model trained successfully!")

# 6️⃣ Evaluate the model
y_pred = model.predict(X_test_bow)

print("\n📊 Model Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 7️⃣ (Optional) Save model and vectorizer
os.makedirs(r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Models", exist_ok=True)

with open(r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Models\bow_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(r"C:\Users\Mohamed Yousuf\Downloads\Professional\ToxicCommentDetection\Models\logreg_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n💾 Model and vectorizer saved successfully!")
