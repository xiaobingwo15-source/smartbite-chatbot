# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SmartBite — a Malaysian restaurant chatbot ("Warung SmartBite") for a TARUMT AI assignment. Two members each build a chatbot using different approaches, sharing the same intent schema and menu data for fair comparison.

- **Member 1:** ML-based chatbot using Rasa Open Source 3.x (Python)
- **Member 2:** Platform-based chatbot using Pandorabots (AIML)
- **Deadline:** 28 August 2026

## Commands

### Member 1 (Rasa)

```bash
cd member1_rasa

# Install dependencies (use a venv)
pip install -r requirements.txt

# Train the model
rasa train

# Run NLU training only
rasa train nlu

# Test NLU with cross-validation
rasa test nlu

# Interactive training (debug stories)
rasa interactive

# Talk to the bot in terminal
rasa shell

# Start the action server (required for custom actions)
rasa run actions

# Run the full server (API mode)
rasa run --enable-api --cors "*"
```

The action server must be running on `localhost:5055` for custom actions to work (configured in `endpoints.yml`).

### Member 2 (Pandorabots)

Pandorabots is a web platform — no local build step. AIML files are uploaded via the Pandorabots dashboard or API. Testing is done through the platform's debugger or REST API.

## Architecture

### Shared Data Layer

`shared/menu_data.json` is the single source of truth for the restaurant menu. Both chatbots reference this file. It contains:
- Restaurant metadata (name, hours, location, payment methods)
- 25 menu items across 5 categories (rice, noodles, snacks, drinks, desserts)
- Each item has: name, category, price, description, spicy/vegetarian flags, tags

Rasa loads this file at runtime via `actions/actions.py` using a relative path (`../../shared/menu_data.json` from the actions directory).

### Member 1: Rasa Project Structure

```
member1_rasa/
├── data/
│   ├── nlu.yml          # 21 intents, ~15-20 examples each (Malay + English)
│   ├── stories.yml      # Conversation flow examples
│   └── rules.yml        # FAQ-style single-turn responses
├── actions/
│   ├── actions.py       # 7 custom actions (order CRUD, menu, recommend, complaints)
│   └── menu_data.py     # Menu data helper
├── domain.yml           # Intents, entities, slots, responses, action declarations
├── config.yml           # NLU pipeline (DIET) + dialogue policies (TED, RulePolicy)
├── endpoints.yml        # Action server endpoint (localhost:5055)
└── requirements.txt     # Python dependencies
```

**Key architectural decisions:**
- DIET classifier handles both intent classification and entity extraction in a single pipeline
- TED policy manages multi-turn dialogue
- Order state is stored in the `order_list` slot (list type, not influenced by conversation)
- Custom actions in `actions.py` load menu data from `shared/menu_data.json` at runtime
- Fuzzy item matching: exact match first, then substring fallback

### Intent Schema (21 intents, shared across both chatbots)

Core groups: `greet`/`goodbye`/`thanks`, `menu_browse`/`menu_ask_price`, `order_place`/`order_modify`/`order_cancel`/`order_check`, `recommend`/`recommend_spicy`/`recommend_vegetarian`/`recommend_budget`, `dietary_info`, `complaint_food`/`complaint_service`/`complaint_other`, `ask_hours`/`ask_location`/`ask_reservation`/`ask_payment`.

### Entities

`food_item`, `category`, `quantity`, `preference`, `budget` — extracted by DIET from NLU training data.

### Member 2: Pandorabots Structure

```
member2_pandorabots/
├── aiml/                # AIML category files (one per intent group)
├── web/                 # Custom HTML/CSS/JS chat frontend
├── tests/               # Test queries + evaluation script
└── requirements.txt     # Python deps for testing only
```

See `IMPLEMENTATION_PLAN.md` for the full Member 2 implementation plan.

## Evaluation

Both chatbots are evaluated on the same metrics: intent accuracy, precision, recall, F1, BLEU, ROUGE-L, response time, and user satisfaction. Results are compared in the documentation.

## Key Files to Read First

1. `IMPLEMENTATION_PLAN.md` — full project plan, timeline, intent schema, evaluation plan
2. `shared/menu_data.json` — restaurant menu data
3. `member1_rasa/domain.yml` — all intents, entities, slots, responses
4. `member1_rasa/actions/actions.py` — custom action implementations
5. `member1_rasa/data/nlu.yml` — NLU training examples
