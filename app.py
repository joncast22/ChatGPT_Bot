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
    metadata={"email": email},  # Possible issue here
)
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
    metadata={"email": str(email) if email else "unknown"},  # Fix metadata issue
)
