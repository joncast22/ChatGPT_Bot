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
   @app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        data = request.json  # Get the request body
        email = data.get("email", None)  # Extract email

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
            metadata={"email": str(email)},  # Fix: Convert `email` to a string
        )

        return jsonify({"checkout_url": session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

