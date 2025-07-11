from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

OLLAMA_API = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"  # You can switch to mistral, llama3, etc.

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({"response": "No input received"}), 400

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_input,
        "stream": True
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, stream=True)
        full_reply = ""
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                full_reply += chunk.get("response", "")
                if chunk.get("done", False):
                    break
        return jsonify({"response": full_reply})
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)