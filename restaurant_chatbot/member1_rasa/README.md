# SmartBite Malaysian Restaurant Chatbot

A ML-based chatbot for a Malaysian restaurant, built with Python, Flask, and scikit-learn.

## Features

- **Intent Classification**: TF-IDF + LinearSVC for understanding user intents
- **Entity Extraction**: Pattern matching and fuzzy matching for food items, categories, quantities
- **Order Management**: Add, modify, check, and cancel orders
- **Menu Browsing**: Browse full menu or by category
- **Recommendations**: Spicy, vegetarian, and budget-friendly suggestions
- **Restaurant Info**: Hours, location, reservations, payment methods

## Project Structure

```
restaurant_chatbot/
├── member1_rasa/
│   ├── chatbot/           # Main chatbot module
│   │   ├── chatbot.py     # Main chatbot class
│   │   ├── intent_classifier.py  # ML intent classification
│   │   └── entity_extractor.py   # Entity extraction
│   ├── web/               # Flask web server
│   │   ├── app.py         # Flask application
│   │   ├── index.html     # Frontend UI
│   │   └── style.css      # Styles
│   ├── data/              # Training data
│   │   └── training_data.json
│   ├── models/            # Trained models
│   ├── actions/           # Rasa actions (if using Rasa)
│   ├── config.yml         # Rasa configuration
│   ├── domain.yml         # Rasa domain
│   ├── requirements.txt   # Python dependencies
│   └── train_model.py     # Model training script
└── shared/
    └── menu_data.json     # Restaurant menu data
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/WoXiaoBing/smartbite-chatbot.git
cd smartbite-chatbot/restaurant_chatbot/member1_rasa
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface
```bash
cd web
python app.py
```
Open http://localhost:5005 in your browser.

### Terminal Mode
```bash
python chatbot/chatbot.py
```

## Supported Intents

| Intent | Example |
|--------|---------|
| greet | "hello", "hi" |
| goodbye | "bye", "see you" |
| menu_browse | "show me the menu" |
| menu_ask_price | "how much is nasi lemak" |
| order_place | "I want nasi lemak" |
| order_check | "what is my order" |
| order_cancel | "cancel my order" |
| recommend | "recommend something" |
| recommend_spicy | "recommend something spicy" |
| recommend_vegetarian | "recommend vegetarian food" |
| recommend_budget | "recommend food under RM10" |
| ask_hours | "what are your hours" |
| ask_location | "where are you located" |
| ask_reservation | "how to make reservation" |
| ask_payment | "what payment methods" |

## Menu Categories

- **Rice**: Nasi Lemak, Nasi Goreng, Nasi Kandar, etc.
- **Noodles**: Mee Goreng, Char Kuey Teow, Laksa, etc.
- **Snacks**: Roti Canai, Satay, Popiah, etc.
- **Drinks**: Teh Tarik, Kopi, Sirap Bandung, etc.
- **Desserts**: Cendol, Ais Kacang, Kuih-muih, etc.

## Technologies

- Python 3.11+
- Flask (Web framework)
- scikit-learn (Machine learning)
- TF-IDF + LinearSVC (Intent classification)
- FuzzyWuzzy (Entity extraction)

## License

This project is for educational purposes (TARUMT AI Assignment).
