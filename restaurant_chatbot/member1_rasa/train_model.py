"""
Train the intent classifier model.
Run this script to train and evaluate the ML model.
"""

import os
import sys

# Add chatbot directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chatbot'))

from intent_classifier import IntentClassifier


def main():
    """Train and evaluate the intent classifier."""
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Paths
    training_data_path = os.path.join(base_path, 'data', 'training_data.json')
    model_path = os.path.join(base_path, 'models', 'intent_classifier.pkl')

    # Create models directory
    os.makedirs(os.path.join(base_path, 'models'), exist_ok=True)

    # Initialize and train
    classifier = IntentClassifier()
    classifier.load_training_data(training_data_path)

    # Train with evaluation
    metrics = classifier.train(test_size=0.15, random_state=42)

    # Save model
    classifier.save(model_path)

    # Print summary
    print("\n" + "=" * 50)
    print("TRAINING COMPLETE")
    print("=" * 50)
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Macro F1: {metrics['macro_f1']:.4f}")
    print(f"Weighted F1: {metrics['weighted_f1']:.4f}")
    print(f"Training samples: {metrics['train_size']}")
    print(f"Test samples: {metrics['test_size']}")
    print(f"\nModel saved to: {model_path}")

    # Test some predictions
    print("\n" + "=" * 50)
    print("SAMPLE PREDICTIONS")
    print("=" * 50)

    test_inputs = [
        "hi there",
        "show me the menu",
        "I want nasi lemak",
        "something spicy",
        "how much is satay",
        "where are you located",
        "cancel my order",
        "thank you",
        "I have a complaint about the food",
        "what time do you close"
    ]

    for text in test_inputs:
        intent, confidence = classifier.predict(text)
        print(f"  '{text}' -> {intent} ({confidence:.2f})")


if __name__ == '__main__':
    main()
