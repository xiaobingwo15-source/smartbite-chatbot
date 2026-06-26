"""
Intent Classifier for SmartBite Chatbot.
Uses TF-IDF vectorization + LinearSVC for intent recognition.
This approach demonstrates ML-based NLP without relying on Rasa.
"""

import json
import os
import re
import string
from typing import Dict, List, Optional, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline


class IntentClassifier:
    """ML-based intent classifier using TF-IDF + LinearSVC."""

    def __init__(self, model_path: Optional[str] = None):
        self.pipeline: Optional[Pipeline] = None
        self.intent_labels: List[str] = []
        self.training_data: Dict[str, List[str]] = {}

        if model_path and os.path.exists(model_path):
            self.load(model_path)

    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize input text."""
        text = text.lower().strip()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^\w\s?!]', '', text)
        return text

    def load_training_data(self, data_path: str) -> None:
        """Load training data from JSON file."""
        with open(data_path, 'r', encoding='utf-8') as f:
            self.training_data = json.load(f)
        self.intent_labels = sorted(self.training_data.keys())
        print(f"[INFO] Loaded {len(self.intent_labels)} intents with "
              f"{sum(len(v) for v in self.training_data.values())} total examples")

    def train(self, test_size: float = 0.15, random_state: int = 42) -> Dict:
        """Train the intent classifier and return evaluation metrics."""
        if not self.training_data:
            raise ValueError("No training data loaded. Call load_training_data() first.")

        # Prepare dataset
        texts = []
        labels = []
        for intent, examples in self.training_data.items():
            for example in examples:
                texts.append(self._preprocess_text(example))
                labels.append(intent)

        # Split for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state, stratify=labels
        )

        # Build pipeline: TF-IDF + LinearSVC
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                analyzer='word',
                ngram_range=(1, 2),
                max_features=5000,
                sublinear_tf=True
            )),
            ('classifier', LinearSVC(
                C=1.0,
                max_iter=10000,
                class_weight='balanced',
                random_state=random_state
            ))
        ])

        # Train
        print("[INFO] Training intent classifier...")
        self.pipeline.fit(X_train, y_train)

        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)
        report_text = classification_report(y_test, y_pred)

        print("\n[EVALUATION RESULTS]")
        print(report_text)

        return {
            'accuracy': report['accuracy'],
            'macro_f1': report['macro avg']['f1-score'],
            'weighted_f1': report['weighted avg']['f1-score'],
            'report': report_text,
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'test_size': len(X_test),
            'train_size': len(X_train)
        }

    def predict(self, text: str) -> Tuple[str, float]:
        """Predict intent for a given text. Returns (intent, confidence)."""
        if not self.pipeline:
            raise ValueError("Model not trained. Call train() or load() first.")

        processed = self._preprocess_text(text)
        intent = self.pipeline.predict([processed])[0]

        # Get confidence from decision function
        decision_scores = self.pipeline.decision_function([processed])
        max_score = np.max(decision_scores)
        # Convert to pseudo-confidence using sigmoid
        confidence = 1 / (1 + np.exp(-max_score))

        return intent, float(confidence)

    def predict_top_n(self, text: str, n: int = 3) -> List[Tuple[str, float]]:
        """Predict top N intents with confidence scores."""
        if not self.pipeline:
            raise ValueError("Model not trained. Call train() or load() first.")

        processed = self._preprocess_text(text)
        decision_scores = self.pipeline.decision_function([processed])[0]

        # Get top N indices
        top_indices = np.argsort(decision_scores)[-n:][::-1]
        results = []
        for idx in top_indices:
            intent = self.pipeline.classes_[idx]
            confidence = 1 / (1 + np.exp(-decision_scores[idx]))
            results.append((intent, float(confidence)))

        return results

    def save(self, model_path: str) -> None:
        """Save the trained model to disk."""
        if not self.pipeline:
            raise ValueError("No model to save.")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'pipeline': self.pipeline,
            'intent_labels': self.intent_labels
        }, model_path)
        print(f"[INFO] Model saved to {model_path}")

    def load(self, model_path: str) -> None:
        """Load a trained model from disk."""
        data = joblib.load(model_path)
        self.pipeline = data['pipeline']
        self.intent_labels = data['intent_labels']
        print(f"[INFO] Model loaded from {model_path}")


if __name__ == '__main__':
    # Demo training
    classifier = IntentClassifier()
    classifier.load_training_data('../data/training_data.json')
    metrics = classifier.train()
    print(f"\nAccuracy: {metrics['accuracy']:.4f}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")
