import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# API Key (⚠️ WARNING: Storing API key in code is insecure! Use environment variables.)
API_KEY = "AIzaSyB_oO5sCAv6Vvbo7tIPRmUVxMcQFgdUNcE"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={API_KEY}"

# Initialize Flask app
app = Flask(__name__)

# Allow CORS from all origins (Frontend can connect)
CORS(app, resources={r"/chat": {"origins": "*"}})

def get_response(user_input):
    """ Sends user input to Gemini AI API and returns the response """
    payload = {"contents": [{"parts": [{"text": user_input}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract AI response
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received.")
        return "🤖 Gemini AI: No response received."

    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    """ API endpoint for chatbot interaction """
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "❌ Error: Empty message received"}), 400

    response_text = get_response(user_input)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Allow access from any IP
