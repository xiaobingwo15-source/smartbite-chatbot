# Evaluation Results

This directory stores evaluation metrics and reports for both chatbots.

## Expected Files

After running evaluation, this folder should contain:

### Member 1 (Rasa)
- `member1_nlu_evaluation.json` — NLU classification report (precision, recall, F1 per intent)
- `member1_confusion_matrix.png` — Confusion matrix visualization
- `member1_intent_errors.json` — Misclassified examples
- `member1_entity_evaluation.json` — Entity extraction scores
- `member1_response_evaluation.json` — End-to-end dialogue evaluation

### Member 2 (Pandorabots)
- `member2_test_results.json` — Test query results
- `member2_accuracy_report.txt` — Overall accuracy metrics
- `member2_confusion_matrix.png` — Confusion matrix

### Comparison
- `comparison_table.md` — Side-by-side comparison of both chatbots
- `metrics_summary.csv` — Combined metrics in tabular format

## How to Generate

### Rasa NLU Evaluation

```bash
cd member1_rasa

# Train model first (if not already trained)
rasa train

# Run NLU evaluation with cross-validation
rasa test nlu --nlu data/nlu.yml --out ../shared/evaluation_results/member1

# Run end-to-end story evaluation
rasa test core --stories data/stories.yml --out ../shared/evaluation_results/member1
```

### Using the Test Queries

The `shared/test_queries.csv` file contains 1074 test queries (50+ per intent) that can be used to evaluate both chatbots programmatically.

## Metrics to Report

For the documentation, include:
1. **Intent Classification**: Precision, Recall, F1-score per intent
2. **Entity Extraction**: Entity-level precision, recall, F1
3. **Confusion Matrix**: Visual representation of misclassifications
4. **Response Accuracy**: End-to-end correctness of chatbot responses
5. **Comparison Table**: Rasa vs Pandorabots side-by-side
