from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Chatbot is running! Visit /subscribe to sign up."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
