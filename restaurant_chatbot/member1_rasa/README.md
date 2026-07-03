# SmartBite Restaurant Chatbot — Member 1 (Rasa)

A conversational AI chatbot for **Warung SmartBite**, a Malaysian restaurant, built using [Rasa 3.x](https://rasa.com/).

## Architecture

```
member1_rasa/
├── actions/
│   ├── actions.py          # 7 custom Rasa actions
│   └── menu_data.py        # Menu data helper utilities
├── chatbot/                # Standalone sklearn-based chatbot (bonus)
│   ├── chatbot.py
│   ├── intent_classifier.py
│   └── entity_extractor.py
├── data/
│   ├── nlu.yml             # NLU training data (350+ examples, 21 intents)
│   ├── stories.yml         # 15 multi-turn conversation stories
│   ├── rules.yml           # 11 single-turn rules
│   └── training_data.json  # Training data for standalone classifier
├── models/                 # Trained Rasa model (gitignored)
├── web/
│   ├── app.py              # Flask web UI (proxies to Rasa REST API)
│   ├── index.html          # Chat interface
│   └── style.css           # Styling
├── config.yml              # Rasa pipeline & policy configuration
├── credentials.yml         # Channel credentials (REST)
├── domain.yml              # Intents, entities, slots, responses, actions
├── endpoints.yml           # Action server endpoint
└── requirements.txt        # Python dependencies
```

## Intents (21)

| Category | Intents |
|----------|---------|
| **Greeting** | `greet`, `goodbye`, `thanks` |
| **Menu** | `menu_browse`, `menu_ask_price` |
| **Ordering** | `order_place`, `order_modify`, `order_cancel`, `order_check` |
| **Recommendations** | `recommend`, `recommend_spicy`, `recommend_vegetarian`, `recommend_budget` |
| **Information** | `dietary_info`, `ask_hours`, `ask_location`, `ask_reservation`, `ask_payment` |
| **Complaints** | `complaint_food`, `complaint_service`, `complaint_other` |

## Custom Actions (7)

| Action | Description |
|--------|-------------|
| `action_place_order` | Add item to order with quantity, validates against menu |
| `action_modify_order` | Change, remove, or add more items to existing order |
| `action_cancel_order` | Cancel the entire order |
| `action_check_order` | Display itemized receipt with running total |
| `action_show_menu_by_category` | Filter menu by category (rice/noodles/snacks/drinks/desserts) |
| `action_recommend_dish` | Recommend dishes by preference (spicy/vegetarian/budget/popular) |
| `action_handle_complaint` | Handle complaints with empathy and offer solutions |

## Setup & Running

### Prerequisites
- Python 3.8–3.10 (Rasa 3.x compatibility)
- pip

### Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Training

```bash
# Train the Rasa model
rasa train
```

### Running

You need **3 terminals**:

```bash
# Terminal 1: Start Rasa server (with REST API)
rasa run --enable-api --cors "*" --port 5005

# Terminal 2: Start action server
rasa run actions --port 5055

# Terminal 3: Start web UI
python web/app.py
# Open http://localhost:5006 in your browser
```

### Quick Test (CLI)

```bash
# Test interactively via command line
rasa shell
```

### NLU Evaluation

```bash
# Evaluate NLU with cross-validation
rasa test nlu --nlu data/nlu.yml

# Results saved to results/ directory
```

## NLU Pipeline

| Component | Purpose |
|-----------|---------|
| `WhitespaceTokenizer` | Tokenize by whitespace |
| `RegexFeaturizer` | Regex-based features |
| `LexicalSyntacticFeaturizer` | Lexical/syntactic features |
| `CountVectorsFeaturizer` | Word-level bag-of-words |
| `CountVectorsFeaturizer` (char_wb) | Character n-gram features |
| `DIETClassifier` | Intent classification + entity extraction |
| `EntitySynonymMapper` | Map entity synonyms |
| `ResponseSelector` | Select response templates |
| `FallbackClassifier` | Catch low-confidence predictions (threshold 0.3) |

## Dialogue Policies

| Policy | Purpose |
|--------|---------|
| `MemoizationPolicy` | Memorize training stories |
| `RulePolicy` | Handle single-turn rules (fallback threshold 0.4) |
| `TEDPolicy` | Transformer-based dialogue policy (max_history=5) |

## Menu Data

The chatbot uses a shared menu dataset (`../shared/menu_data.json`) with 25 Malaysian dishes across 5 categories:
- 🍚 **Rice** (6 items): Nasi Lemak, Nasi Goreng, Nasi Kandar, etc.
- 🍜 **Noodles** (5 items): Mee Goreng, Char Kuey Teow, Laksa, etc.
- 🍢 **Snacks** (5 items): Roti Canai, Satay, Popiah, etc.
- ☕ **Drinks** (5 items): Teh Tarik, Kopi, Sirap Bandung, etc.
- 🍧 **Desserts** (4 items): Cendol, Ais Kacang, Kuih-muih, Pengat

## License

This project is part of a TARUMT AI assignment (2026).
