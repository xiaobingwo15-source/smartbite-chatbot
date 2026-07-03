# SmartBite — Malaysian Restaurant Chatbot
## Implementation Plan

---

## Project Overview

| Item | Detail |
|---|---|
| **Project Name** | SmartBite — Malaysian Restaurant Chatbot |
| **Scenario** | Malaysian restaurant chatbot for ordering, FAQ, and recommendations |
| **Group Size** | 2 members |
| **Member 1** | ML-based chatbot using Rasa Open Source |
| **Member 2** | Platform-based chatbot using Pandorabots |
| **Deadline** | 28 August 2026 (Week 11, Friday, before 12pm) |
| **Demo** | Week 12-14, each member presents their own chatbot |

---

## Restaurant Profile

**"Warung SmartBite"** — A Malaysian restaurant serving:

| Category | Items |
|---|---|
| **Rice Dishes** | Nasi Lemak, Nasi Goreng, Nasi Kandar, Nasi Kerabu |
| **Noodles** | Mee Goreng, Char Kuey Teow, Laksa, Curry Mee |
| **Snacks** | Roti Canai, Satay, Popiah, Curry Puff |
| **Drinks** | Teh Tarik, Kopi, Sirap Bandung, Milo Ais |
| **Desserts** | Cendol, Ais Kacang, Kuih-muih |

---

## Functionalities (All 3 Categories)

### 1. FAQ (Answering Questions)
- Restaurant hours, location, contact info
- Menu items and prices
- Dietary info (halal, vegetarian options)
- Payment methods accepted
- Reservation policies

### 2. Natural Conversation
- Greeting and goodbye
- Small talk (how are you, thanks)
- Clarification when input is unclear
- Context retention across conversation turns

### 3. Recommendations / Orders / Complaints
- Recommend dishes based on preferences (spicy, sweet, vegetarian)
- Take orders (add/remove items, modify quantities)
- Handle complaints (wrong order, cold food, long wait)
- Suggest combos and promotions

---

## Intent Schema (Shared Dataset)

Both chatbots will use the **same intent set** for fair comparison:

| Intent | Example Utterances | Response Type |
|---|---|---|
| `greet` | "hi", "hello", "hey", "selamat pagi" | Friendly greeting |
| `goodbye` | "bye", "thanks", "see you", "terima kasih" | Farewell |
| `menu_browse` | "show menu", "what do you have", "what's available" | Display menu categories |
| `menu_ask_price` | "how much is nasi lemak", "price of satay" | Return item price |
| `order_place` | "I want to order", "I'll have nasi lemak", "add satay" | Confirm order |
| `order_modify` | "change to mee goreng", "remove the drink", "add one more" | Update order |
| `order_cancel` | "cancel my order", "nevermind", "forget it" | Cancel order |
| `order_check` | "what did I order", "show my order", "current order" | Display order summary |
| `recommend` | "what do you recommend", "suggest something", "popular dishes" | Give recommendations |
| `recommend_spicy` | "something spicy", "I like it hot" | Spicy dish suggestions |
| `recommend_vegetarian` | "vegetarian options", "no meat please" | Vegetarian suggestions |
| `recommend_budget` | "something cheap", "budget meal", "under RM10" | Budget suggestions |
| `dietary_info` | "is it halal", "any gluten-free", "allergens" | Dietary information |
| `complaint_food` | "food is cold", "wrong order", "tastes bad" | Apologize + offer solution |
| `complaint_service` | "waiting too long", "slow service" | Apologize + escalate |
| `complaint_other` | "dirty table", "rude staff" | Apologize + log complaint |
| `ask_hours` | "when are you open", "what time do you close" | Return operating hours |
| `ask_location` | "where are you", "address", "how to get there" | Return location |
| `ask_reservation` | "book a table", "reserve for 4" | Reservation process |
| `ask_payment` | "do you accept card", "payment methods" | Payment info |
| `thanks` | "thank you", "thanks a lot", "appreciate it" | Acknowledge thanks |

**Total: 21 intents**

---

## Entity Schema

| Entity | Examples | Type |
|---|---|---|
| `food_item` | nasi lemak, satay, teh tarik | Lookup |
| `category` | rice, noodles, snacks, drinks, desserts | Lookup |
| `quantity` | one, two, 3, a dozen | Number |
| `preference` | spicy, sweet, vegetarian, halal | Lookup |
| `budget` | cheap, expensive, under RM10 | Lookup |

---

## Member 1: ML-Based Chatbot (Rasa)

### Tech Stack
- **Framework:** Rasa Open Source 3.x
- **Language:** Python 3.10+
- **NLU:** Rasa's DIET classifier (intent + entity extraction)
- **Dialogue:** Rasa's TED policy (transformer-based dialogue management)
- **Frontend:** Simple Python terminal UI or Flask web UI

### Implementation Steps

#### Phase 1: Setup & Data Preparation (Week 1-2)
1. Install Rasa (`pip install rasa`)
2. Initialize Rasa project (`rasa init`)
3. Create training data:
   - `nlu.yml` — 15-20 example utterances per intent (300+ total)
   - `domain.yml` — intents, entities, responses, actions
   - `stories.yml` — conversation flow examples
   - `rules.yml` — FAQ-style single-turn responses
4. Create custom actions (`actions.py`):
   - `ActionPlaceOrder` — manage order state
   - `ActionRecommendDish` — suggest based on preference
   - `ActionShowMenu` — return menu by category
   - `ActionCheckOrder` — display current order

#### Phase 2: Model Training & Tuning (Week 3-4)
1. Train NLU model (`rasa train nlu`)
2. Evaluate NLU with cross-validation (`rasa test nlu`)
3. Train dialogue model (`rasa train`)
4. Test in interactive mode (`rasa interactive`)
5. Tune hyperparameters:
   - DIET epochs, batch size
   - TED policy max history
   - Augmentation factor

#### Phase 3: Integration & Testing (Week 5-6)
1. Build simple web UI (Flask or Rasa's built-in channel)
2. Run `rasa shell` for terminal testing
3. Create test dataset (50+ test queries per intent)
4. Generate evaluation reports:
   - Confusion matrix
   - Intent classification report (precision, recall, F1)
   - Entity extraction scores

#### Phase 4: Polish & Documentation (Week 7-8)
1. Add error handling for unrecognized inputs
2. Implement fallback responses
3. Add conversation context retention
4. Export evaluation metrics for comparison
5. Document code with comments

### Key Files
```
member1_rasa/
├── data/
│   ├── nlu.yml              # Training intents
│   ├── stories.yml          # Conversation flows
│   └── rules.yml            # FAQ rules
├── actions/
│   ├── actions.py           # Custom actions
│   └── menu_data.py         # Restaurant menu data
├── models/                  # Trained models
├── tests/
│   ├── test_stories.yml     # Story tests
│   └── test_nlu.py          # NLU evaluation
├── domain.yml               # Domain definition
├── config.yml               # Pipeline config
├── endpoints.yml            # Action server config
├── requirements.txt         # Dependencies
└── README.md                # Setup instructions
```

---

## Member 2: Platform-Based Chatbot (Pandorabots)

### Tech Stack
- **Platform:** Pandorabots (https://www.pandorabots.com/)
- **Language:** AIML (Artificial Intelligence Markup Language)
- **Frontend:** Pandorabots web widget or custom HTML/JS embed

### Implementation Steps

#### Phase 1: Setup & AIML Design (Week 1-2)
1. Create Pandorabots account
2. Create new bot project
3. Design AIML category structure:
   - `greet.aiml` — greeting patterns
   - `menu.aiml` — menu browsing patterns
   - `order.aiml` — ordering patterns
   - `recommend.aiml` — recommendation patterns
   - `complaint.aiml` — complaint handling patterns
   - `faq.aiml` — FAQ patterns
4. Write AIML patterns with wildcards and sets:
   ```xml
   <category>
     <pattern>I WANT TO ORDER *</pattern>
     <template>
       <srai>ORDER <star/></srai>
     </template>
   </category>
   ```

#### Phase 2: Core Bot Development (Week 3-4)
1. Implement all 21 intents as AIML categories
2. Create `<set>` and `<get>` tags for order state management
3. Build recommendation logic using AIML conditions:
   ```xml
   <category>
     <pattern>RECOMMEND SPICY</pattern>
     <template>
       <condition>
         <li value="ordered">Since you ordered rice, try Nasi Goreng Kampung!</li>
         <li>Try our Laksa or Curry Mee — both are spicy and delicious!</li>
       </condition>
     </template>
   </category>
   ```
4. Add entity recognition with AIML `<set>` definitions
5. Implement context tracking with `<that>` tags

#### Phase 3: Testing & Refinement (Week 5-6)
1. Test all intents in Pandorabots debugger
2. Create test script (Python + Pandorabots API):
   - Send test queries via REST API
   - Compare responses to expected outputs
   - Calculate accuracy metrics
3. Refine patterns based on test failures
4. Add fallback responses for unrecognized input

#### Phase 4: API Integration & Polish (Week 7-8)
1. Integrate Pandorabots API into custom frontend:
   - HTML/CSS chat interface
   - JavaScript for API calls
   - Display order summary
2. Add external API integration (optional):
   - Order tracking
   - Simple database for order history
3. Generate evaluation metrics:
   - Intent recognition accuracy (via test queries)
   - Response relevancy (manual scoring)
   - User satisfaction (survey)

### Key Files
```
member2_pandorabots/
├── aiml/
│   ├── greet.aiml           # Greeting patterns
│   ├── menu.aiml            # Menu browsing
│   ├── order.aiml           # Ordering flow
│   ├── recommend.aiml       # Recommendations
│   ├── complaint.aiml       # Complaint handling
│   ├── faq.aiml             # FAQ responses
│   ├── context.aiml         # Context management
│   └── sets/
│       ├── food_items.set   # Food item entity
│       ├── categories.set   # Menu categories
│       └── preferences.set  # Preference entities
├── web/
│   ├── index.html           # Chat UI
│   ├── style.css            # Styling
│   ├── script.js            # API integration
│   └── api_config.js        # Pandorabots API keys
├── tests/
│   ├── test_queries.csv     # Test dataset
│   ├── test_results.csv     # Test outputs
│   └── evaluate.py          # Evaluation script
├── requirements.txt         # Python dependencies (for testing)
└── README.md                # Setup instructions
```

---

## Shared Dataset

### Menu Data (JSON)
```json
{
  "restaurant": {
    "name": "Warung SmartBite",
    "cuisine": "Malaysian",
    "halal": true,
    "hours": "10:00 AM - 10:00 PM (Daily)",
    "location": "TARUMT Campus, Setapak, Kuala Lumpur",
    "payment": ["Cash", "Touch 'n Go", "GrabPay", "Debit/Credit Card"]
  },
  "menu": [
    {
      "name": "Nasi Lemak",
      "category": "rice",
      "price": 8.50,
      "description": "Coconut rice with sambal, anchovies, peanuts, egg",
      "spicy": true,
      "vegetarian": false,
      "tags": ["popular", "signature"]
    },
    {
      "name": "Roti Canai",
      "category": "snacks",
      "price": 3.50,
      "description": "Flaky flatbread with dhal or curry",
      "spicy": false,
      "vegetarian": true,
      "tags": ["breakfast", "popular"]
    }
    // ... more items
  ]
}
```

### Test Queries (CSV)
- 50+ test queries per intent (1050+ total)
- Covers variations, typos, colloquial Malay/English
- Used for both chatbots' evaluation

---

## Evaluation Plan

### Metrics to Collect

| Metric | How to Measure | For |
|---|---|---|
| **Intent Accuracy** | Correct intent / Total test queries | Both |
| **Precision** | TP / (TP + FP) per intent | Both |
| **Recall** | TP / (TP + FN) per intent | Both |
| **F1 Score** | 2 × (P × R) / (P + R) | Both |
| **BLEU Score** | Response vs reference response | Both |
| **ROUGE Score** | Response vs reference response | Both |
| **Response Time** | Average time to respond | Both |
| **User Satisfaction** | Survey (1-5 scale) | Both |

### Test Process
1. **Automated Testing:**
   - Run 1050+ test queries through both chatbots
   - Log predicted intent vs actual intent
   - Calculate precision, recall, F1 per intent

2. **Response Quality:**
   - 50 selected queries with reference responses
   - Calculate BLEU and ROUGE scores

3. **User Satisfaction Survey:**
   - 10-15 test users interact with each chatbot
   - Rate: ease of use, response accuracy, overall satisfaction
   - Compare average scores

### Comparison Table (for Documentation)

| Metric | Rasa (ML-Based) | Pandorabots (Platform) | Winner |
|---|---|---|---|
| Intent Accuracy | ? | ? | ? |
| F1 Score (Macro) | ? | ? | ? |
| BLEU Score | ? | ? | ? |
| ROUGE-L | ? | ? | ? |
| Avg Response Time | ? | ? | ? |
| User Satisfaction | ? | ? | ? |

---

## Documentation Structure

### Part 1: Documentation (40%)

| Section | Content | Pages |
|---|---|---|
| **1. Introduction** | Background of restaurant chatbots, problem statement, objectives, significance, research gap | 2-3 |
| **2. Related Work** | Literature review on chatbot technologies, comparison of ML vs platform approaches, gaps | 3-4 |
| **3. Methodology** | System flow, dataset description, Rasa pipeline, AIML structure, evaluation metrics | 4-5 |
| **4. Results & Discussion** | Metrics comparison table, charts, discussion of why one approach outperforms the other | 3-4 |
| **5. Conclusion** | Achievements, limitations, future work | 1-2 |
| **6. References** | APA format — Rasa docs, Pandorabots docs, chatbot research papers | 1 |
| **7. Appendix** | AI Disclosure (Appendix B), Plagiarism Statement (Appendix A), source code listing | 1 |

---

## Timeline

| Week | Dates | Member 1 (Rasa) | Member 2 (Pandorabots) | Shared |
|---|---|---|---|---|
| 1 | - | Install Rasa, design intents | Create Pandorabots account, design AIML | Create shared menu dataset |
| 2 | - | Write NLU training data | Write AIML categories | Define test queries |
| 3 | - | Train NLU model | Implement ordering flow | - |
| 4 | - | Train dialogue model | Implement recommendations | - |
| 5 | - | Build custom actions | Build complaint handling | - |
| 6 | - | Build web UI | Build web UI | - |
| 7 | - | Run evaluations | Run evaluations | Compare results |
| 8 | - | Polish & debug | Polish & debug | Write documentation |
| 9 | - | Final testing | Final testing | Finalize documentation |
| 10 | - | Code review | Code review | Proofread & submit prep |
| 11 | - | **SUBMIT** | **SUBMIT** | **28 Aug 2026** |
| 12-14 | - | **DEMO** | **DEMO** | Q&A session |

---

## File Structure

```
restaurant_chatbot/
├── shared/
│   ├── menu_data.json           # Restaurant menu dataset
│   ├── test_queries.csv         # Shared test dataset
│   └── evaluation_results/      # Both chatbots' metrics
├── member1_rasa/                # Rasa project
│   └── ... (see Member 1 section)
├── member2_pandorabots/         # Pandorabots project
│   └── ... (see Member 2 section)
├── documentation/
│   ├── documentation_template.md
│   ├── documentation_full.md
│   └── references.bib
├── IMPLEMENTATION_PLAN.md       # This file
└── README.md                    # Project overview
```

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Rasa installation issues | High | Use conda environment, check Python version compatibility |
| Pandorabots API limits | Medium | Cache responses, use free tier efficiently |
| Small training dataset | Medium | Data augmentation, use Rasa's augmentation config |
| BLEU/ROUGE scores low | Low | Focus on intent accuracy, note limitations in discussion |
| Time overrun | High | Follow timeline strictly, prioritize core features |

---

## Next Steps

1. ✅ Confirm this plan
2. Create shared dataset (`menu_data.json`, `test_queries.csv`)
3. Member 1: Install Rasa and initialize project
4. Member 2: Create Pandorabots account and start AIML
5. Begin writing documentation (Introduction section)
