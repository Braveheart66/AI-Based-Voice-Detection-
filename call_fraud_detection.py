import os
import string
import pickle
import pandas as pd
import nltk

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --------------------------------------------------
# Constants
# --------------------------------------------------
MODEL_FILE = "fraud_model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

# --------------------------------------------------
# Globals (lazy-loaded for backend inference)
# --------------------------------------------------
_model = None
_vectorizer = None

# --------------------------------------------------
# Text cleaning (shared by training & inference)
# --------------------------------------------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = ''.join(c for c in text if c not in string.punctuation)
    words = text.split()
    words = [w for w in words if w not in stopwords.words("english")]
    return " ".join(words)

# --------------------------------------------------
# Lazy loader (used by FastAPI)
# --------------------------------------------------
def _load_model():
    global _model, _vectorizer

    if _model is None or _vectorizer is None:
        if not os.path.exists(MODEL_FILE) or not os.path.exists(VECTORIZER_FILE):
            raise FileNotFoundError(
                "Model files not found. Run `python call_fraud_detection.py` once to train."
            )

        with open(MODEL_FILE, "rb") as f:
            _model = pickle.load(f)

        with open(VECTORIZER_FILE, "rb") as f:
            _vectorizer = pickle.load(f)

    return _model, _vectorizer

# --------------------------------------------------
# Inference API (USED BY fraud_service.py)
# --------------------------------------------------
def predict_fraud(text: str):
    """
    Predict whether a call/text is fraud.

    Returns:
        prediction (0 = genuine, 1 = fraud)
        fraud_probability (float)
    """
    model, vectorizer = _load_model()

    text = clean_text(text)
    vector = vectorizer.transform([text])

    fraud_proba = model.predict_proba(vector)[0][1]

    # Lower threshold to improve fraud recall
    prediction = 1 if fraud_proba >= 0.25 else 0

    return prediction, float(fraud_proba)

# --------------------------------------------------
# Training code (RUN MANUALLY ONLY)
# --------------------------------------------------
if __name__ == "__main__":
    nltk.download("stopwords")

    print("📥 Loading dataset...")
    data = pd.read_csv("fraud_calls_multilingual.csv")
    data["label"] = data["label"].map({"fraud": 1, "normal": 0})
    data.dropna(inplace=True)

    data["text"] = data["text"].apply(clean_text)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_df=0.95,
        min_df=2
    )

    X = vectorizer.fit_transform(data["text"])
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # --------------------------------------------------
    # Save trained artifacts
    # --------------------------------------------------
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    with open(VECTORIZER_FILE, "wb") as f:
        pickle.dump(vectorizer, f)

    print("\n✅ Model and vectorizer saved successfully.")
    print("🔎 Test Prediction:",
          predict_fraud("Your bank account is blocked share OTP immediately"))
