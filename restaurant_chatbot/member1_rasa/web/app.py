"""
Flask web server for SmartBite Chatbot.

Proxies chat messages to the Rasa REST API so the demo showcases the
full Rasa NLU + dialogue pipeline (not the standalone sklearn chatbot).

Usage:
  1. Start Rasa server:    rasa run --enable-api --cors "*" --port 5005
  2. Start action server:  rasa run actions --port 5055
  3. Start this web UI:    python web/app.py          (serves on port 5006)
  4. Open http://localhost:5006 in your browser
"""

import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
WEB_UI_PORT = 5006

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

app = Flask(__name__, static_folder=".", template_folder=".")
CORS(app)


@app.route("/")
def home():
    """Serve the chat interface."""
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    """Forward user message to Rasa and return the bot response(s)."""
    data = request.json
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please type a message."})

    try:
        # Send message to Rasa REST API
        rasa_payload = {
            "sender": "web_user",
            "message": message,
        }
        resp = requests.post(RASA_API_URL, json=rasa_payload, timeout=30)
        resp.raise_for_status()

        # Rasa returns a list of response objects: [{"text": "..."}, ...]
        rasa_responses = resp.json()

        if not rasa_responses:
            bot_reply = "I didn't get a response. Please try again."
        else:
            # Concatenate all text responses
            texts = [r.get("text", "") for r in rasa_responses if r.get("text")]
            bot_reply = "\n".join(texts) if texts else "I'm not sure how to respond to that."

        return jsonify({"response": bot_reply})

    except requests.ConnectionError:
        return jsonify({
            "response": (
                "Cannot connect to Rasa server. "
                "Please make sure Rasa is running on port 5005:\n"
                "  rasa run --enable-api --cors '*' --port 5005"
            )
        })
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"response": "Sorry, something went wrong. Please try again."})


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint — also pings Rasa."""
    rasa_ok = False
    try:
        r = requests.get("http://localhost:5005/status", timeout=5)
        rasa_ok = r.status_code == 200
    except Exception:
        pass

    return jsonify({
        "status": "ok",
        "chatbot": "SmartBite",
        "rasa_connected": rasa_ok,
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🍽️  SmartBite Chatbot Web Server")
    print("=" * 50)
    print(f"Web UI:     http://localhost:{WEB_UI_PORT}")
    print(f"Rasa API:   {RASA_API_URL}")
    print()
    print("Make sure Rasa and the action server are running first!")
    print("=" * 50 + "\n")
    app.run(host="0.0.0.0", port=WEB_UI_PORT, debug=True)
