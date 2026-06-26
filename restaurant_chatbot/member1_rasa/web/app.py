"""
Flask web server for SmartBite Chatbot.
Serves the chat interface and handles chatbot requests directly (no Rasa dependency).
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# Add chatbot directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'chatbot'))

from chatbot import SmartBiteChatbot

# Initialize Flask app
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Initialize chatbot
base_path = os.path.join(os.path.dirname(__file__), '..')
chatbot = SmartBiteChatbot(base_path)

print("[INFO] SmartBite Chatbot initialized!")


@app.route('/')
def home():
    """Serve the chat interface."""
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle chat messages."""
    data = request.json
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'response': 'Please type a message.'})

    try:
        response = chatbot.process_message(message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'response': 'Sorry, something went wrong. Please try again.'})


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'chatbot': 'SmartBite'})


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🍽️  SmartBite Chatbot Web Server")
    print("=" * 50)
    print("Open http://localhost:5005 in your browser\n")
    app.run(host='0.0.0.0', port=5005, debug=True)
