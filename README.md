# SmartBite — Malaysian Restaurant Chatbot

A TARUMT AI assignment project comparing two chatbot development approaches: **ML-based (Rasa)** and **Platform-based (Pandorabots)** for a Malaysian restaurant ordering and FAQ system.

## Project Structure

```
restaurant_chatbot/
├── shared/
│   └── menu_data.json           # Restaurant menu (shared by both chatbots)
├── member1_rasa/                # ML-based chatbot (Rasa)
│   ├── data/
│   │   ├── nlu.yml              # 21 intents, ~350 training examples
│   │   ├── stories.yml          # Conversation flows
│   │   └── rules.yml            # FAQ rules
│   ├── actions/
│   │   ├── actions.py           # 7 custom actions
│   │   └── menu_data.py         # Menu data helper
│   ├── domain.yml               # Domain definition
│   ├── config.yml               # NLU pipeline + policies
│   ├── endpoints.yml            # Action server config
│   └── requirements.txt
├── member2_pandorabots/         # Platform-based chatbot (Pandorabots)
│   ├── aiml/                    # AIML category files
│   │   ├── greet.aiml
│   │   ├── menu.aiml
│   │   ├── order.aiml
│   │   ├── recommend.aiml
│   │   ├── complaint.aiml
│   │   ├── faq.aiml
│   │   └── sets/                # Entity definitions
│   ├── web/                     # Chat UI
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── tests/                   # Evaluation
│   │   ├── test_queries.csv
│   │   └── evaluate.py
│   └── requirements.txt
├── documentation/               # Assignment report
├── IMPLEMENTATION_PLAN.md       # Full project plan
└── CLAUDE.md                    # Claude Code guidance
```

## Member 1: Rasa (ML-Based)

### Tech Stack
- **Framework:** Rasa Open Source 3.x
- **NLU:** DIET classifier (intent + entity extraction)
- **Dialogue:** TED policy (transformer-based)
- **Custom Actions:** Python (order management, menu, recommendations, complaints)

### Quick Start

```bash
cd member1_rasa

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Train the model
rasa train

# Start action server (in a separate terminal)
rasa run actions

# Talk to the bot
rasa shell
```

### Custom Actions

| Action | Purpose |
|--------|---------|
| `action_place_order` | Add item to order with quantity validation |
| `action_modify_order` | Change, remove, or increase item quantities |
| `action_cancel_order` | Clear the entire order |
| `action_check_order` | Display itemized receipt with total |
| `action_show_menu_by_category` | Filter menu by category (rice, noodles, etc.) |
| `action_recommend_dish` | Suggest dishes by preference (spicy, vegetarian, budget) |
| `action_handle_complaint` | Empathetic responses with solutions by complaint type |

### Key Design Decisions
- Order state managed via `order_list` slot (list type)
- Fuzzy item matching: exact match → substring fallback
- Budget thresholds: ≤RM6 (budget), ≤RM10 (mid)
- Complaint logging via Python logger for operational visibility

---

## Member 2: Pandorabots (Platform-Based)

### Tech Stack
- **Platform:** Pandorabots (https://www.pandorabots.com/)
- **Language:** AIML 2.0 (Artificial Intelligence Markup Language)
- **Frontend:** Custom HTML/CSS/JS with Pandorabots API integration

### Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  MEMBER 2 WORKFLOW                               │
└─────────────────────────────────────────────────────────────────┘

Phase 1: Setup & AIML Design (Week 1-2)
───────────────────────────────────────
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ Create       │────▶│ Design AIML  │────▶│ Write core   │
  │ Pandorabots  │     │ category     │     │ patterns:    │
  │ account      │     │ structure    │     │ greet, menu, │
  └──────────────┘     └──────────────┘     │ order, FAQ   │
                                             └──────────────┘
                                                     │
Phase 2: Core Development (Week 3-4)                 ▼
─────────────────────────────────────        ┌──────────────┐
                                             │ Implement    │
  ┌──────────────┐     ┌──────────────┐     │ all 21       │
  │ Build order  │◀────│ Build        │◀────│ intents as   │
  │ state mgmt   │     │ recommend    │     │ AIML cats    │
  │ (<set>/<get>)│     │ logic        │     └──────────────┘
  └──────┬───────┘     └──────────────┘
         │
         ▼
Phase 3: Testing & Refinement (Week 5-6)
────────────────────────────────────────
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ Test in      │────▶│ Run API      │────▶│ Refine       │
  │ Pandorabots  │     │ test script  │     │ patterns     │
  │ debugger     │     │ (Python)     │     │ based on     │
  └──────────────┘     └──────────────┘     │ failures     │
                                             └──────────────┘
                                                     │
Phase 4: Integration & Polish (Week 7-8)             ▼
──────────────────────────────────────────   ┌──────────────┐
                                             │ Build custom │
  ┌──────────────┐     ┌──────────────┐     │ HTML/CSS/JS  │
  │ Generate     │◀────│ Integrate    │◀────│ chat UI      │
  │ evaluation   │     │ Pandorabots  │     └──────────────┘
  │ metrics      │     │ API          │
  └──────────────┘     └──────────────┘
```

### AIML File Structure

| File | Intents Covered | Pattern Type |
|------|-----------------|--------------|
| `greet.aiml` | `greet`, `goodbye`, `thanks` | Simple pattern matching |
| `menu.aiml` | `menu_browse`, `menu_ask_price` | Wildcards + entity sets |
| `order.aiml` | `order_place`, `order_modify`, `order_cancel`, `order_check` | Stateful (`<set>`/`<get>`) |
| `recommend.aiml` | `recommend`, `recommend_spicy`, `recommend_vegetarian`, `recommend_budget` | Conditional (`<condition>`) |
| `complaint.aiml` | `complaint_food`, `complaint_service`, `complaint_other` | Pattern + `<that>` context |
| `faq.aiml` | `ask_hours`, `ask_location`, `ask_reservation`, `ask_payment`, `dietary_info` | Direct response |

### AIML Pattern Examples

```xml
<!-- Simple greeting -->
<category>
  <pattern>HELLO</pattern>
  <template>Welcome to Warung SmartBite! How can I help you?</template>
</category>

<!-- Wildcard ordering -->
<category>
  <pattern>I WANT TO ORDER *</pattern>
  <template>
    <srai>ORDER <star/></srai>
  </template>
</category>

<!-- Conditional recommendation -->
<category>
  <pattern>RECOMMEND SPICY</pattern>
  <template>
    <condition>
      <li value="ordered">Since you ordered rice, try Nasi Goreng Kampung!</li>
      <li>Try our Laksa or Curry Mee — both are spicy!</li>
    </condition>
  </template>
</category>

<!-- Context tracking with <that> -->
<category>
  <pattern>YES</pattern>
  <that>WOULD YOU LIKE ANYTHING ELSE</that>
  <template>Great! What would you like to order?</template>
</category>
```

### Entity Recognition (AIML Sets)

```xml
<!-- sets/food_items.set -->
<set name="food_items">
  <item>nasi lemak</item>
  <item>satay</item>
  <item>teh tarik</item>
  <!-- ... all 25 menu items -->
</set>

<!-- Usage in patterns -->
<category>
  <pattern>HOW MUCH IS <set name="food_items">*</set></pattern>
  <template>
    <star/> costs <lookup item="<star/>" source="prices"/>.
  </template>
</category>
```

### Order State Management

```xml
<!-- Add item to order -->
<category>
  <pattern>ADD <set name="food_items">*</set></pattern>
  <template>
    <set name="last_item"><star/></set>
    <set name="order_<star/>">1</set>
    Added <star/> to your order! Anything else?
  </template>
</category>

<!-- Check order -->
<category>
  <pattern>MY ORDER</pattern>
  <template>
    Your order: <get name="last_item"/>.
    Would you like to add more items?
  </template>
</category>
```

### Testing & Evaluation

```bash
cd member2_pandorabots

# Install Python dependencies (for testing only)
pip install -r requirements.txt

# Run automated test suite
python tests/evaluate.py

# Output: test_results.csv with predicted vs actual intents
```

### Quick Start

1. Create account at https://www.pandorabots.com/
2. Create new bot project
3. Upload AIML files from `aiml/` directory
4. Test in the Pandorabots debugger
5. Deploy and integrate with web UI (`web/` directory)

---

## Shared Dataset

Both chatbots use the same intent schema (21 intents) and menu data (`shared/menu_data.json`) for fair comparison.

### Menu Categories

| Category | Items | Price Range |
|----------|-------|-------------|
| 🍚 Rice | Nasi Lemak, Nasi Goreng, Nasi Kandar, Nasi Kerabu, Nasi Ayam, Nasi Dagang | RM8.50 - RM12.00 |
| 🍜 Noodles | Mee Goreng, Char Kuey Teow, Laksa, Curry Mee, Mee Rebus | RM8.00 - RM10.00 |
| 🍢 Snacks | Roti Canai, Satay, Popiah, Curry Puff, Pisang Goreng | RM3.50 - RM12.00 |
| ☕ Drinks | Teh Tarik, Kopi, Sirap Bandung, Milo Ais, Air Mata Kucing | RM3.50 - RM5.00 |
| 🍧 Desserts | Cendol, Ais Kacang, Kuih-muih, Pengat | RM5.00 - RM7.00 |

## Evaluation Metrics

| Metric | How Measured |
|--------|--------------|
| Intent Accuracy | Correct predictions / Total test queries |
| Precision, Recall, F1 | Per-intent and macro-averaged |
| BLEU Score | Response vs reference responses |
| ROUGE-L | Response vs reference responses |
| Response Time | Average latency per query |
| User Satisfaction | Survey (1-5 scale) |

## Documentation

| File | Purpose |
|------|---------|
| `documentation/documentation_expanded.md` | Full report (~12k words) |
| `documentation/documentation_full.md` | First draft |
| `documentation/documentation_template.md` | Skeleton template |
| `documentation/requirements_checklist.md` | Assignment requirement tracking |

## Timeline

| Week | Member 1 (Rasa) | Member 2 (Pandorabots) | Shared |
|------|-----------------|------------------------|--------|
| 1-2 | Install Rasa, write NLU data | Create account, write AIML | Menu dataset |
| 3-4 | Train NLU + dialogue | Implement ordering + recommendations | Test queries |
| 5-6 | Build custom actions + UI | Build complaint handling + UI | - |
| 7-8 | Evaluations + polish | Evaluations + polish | Compare results |
| 9-10 | Final testing + code review | Final testing + code review | Documentation |
| 11 | **SUBMIT (28 Aug 2026)** | **SUBMIT** | Google Classroom |
| 12-14 | **DEMO** | **DEMO** | Q&A session |
