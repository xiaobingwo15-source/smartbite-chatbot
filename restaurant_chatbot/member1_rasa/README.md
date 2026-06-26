# SmartBite Chatbot - Member 1 (Rasa ML-Based)

## Setup
1. Python 3.10+ required
2. `pip install -r requirements.txt`
3. `rasa train`
4. `rasa run actions` (in one terminal)
5. `python web/app.py` (in another terminal)
6. `rasa run --enable-api --cors "*"` (in third terminal)
7. Open http://localhost:5005

## Testing
- `rasa shell` — terminal chat
- `rasa test nlu` — NLU evaluation
- `rasa test core` — story evaluation

## Project Structure
- `config.yml` — Rasa NLU pipeline and dialogue policy configuration
- `endpoints.yml` — Action server endpoint configuration
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation and setup instructions
