from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Chatbot is running! Visit /subscribe to sign up."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
import os
import stripe
import secrets
import sqlite3
from flask import Flask, request, jsonify, redirect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe.api_key = STRIPE_SECRET_KEY

# Database setup
conn = sqlite3.connect("api_keys.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS api_keys (
    email TEXT PRIMARY KEY,
    api_key TEXT
)
""")
conn.commit()

def generate_api_key():
    return secrets.token_hex(16)

def store_api_key(email, api_key):
    cursor.execute("REPLACE INTO api_keys (email, api_key) VALUES (?, ?)", (email, api_key))
    conn.commit()

def get_api_key(email):
    cursor.execute("SELECT api_key FROM api_keys WHERE email = ?", (email,))
    result = cursor.fetchone()
    return result[0] if result else None

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            success_url="https://yourbot.onrender.com/payment-success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourbot.onrender.com/payment-cancel",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": "API Access"},
                        "unit_amount": 500,  # $5.00
                    },
                    "quantity": 1,
                }
            ],
            metadata={"email": email},
        )

        return jsonify({"checkout_url": session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/payment-success", methods=["GET"])
def payment_success():
    session_id = request.args.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)
    email = session.metadata["email"]

    if not email:
        return jsonify({"error": "Email not found"}), 400

    api_key = generate_api_key()
    store_api_key(email, api_key)

    return jsonify({"message": "Payment successful! Your API key has been generated.", "api_key": api_key})

@app.route("/payment-cancel", methods=["GET"])
def payment_cancel():
    return jsonify({"message": "Payment was canceled."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
