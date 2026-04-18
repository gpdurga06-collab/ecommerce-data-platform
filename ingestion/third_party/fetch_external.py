# imports
# Correct — need the whole module
import random
import uuid
import requests



API_URL = "http://localhost:8000/orders"
TOTAL_ORDERS = 100000

# ─── Data ───
PRODUCTS = [
    {"id": 1, "name": "Widget A", "price": 10.0},
    {"id": 2, "name": "Widget B", "price": 20.0},
    {"id": 3, "name": "Widget C", "price": 30.0},
]
CUSTOMERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
]



    
def generate_order():
    product = random.choice(PRODUCTS)
    customer = random.choice(CUSTOMERS)
    return {
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "customer_id": f"CUST-{customer['id']:03d}",
        "product": product["name"],
        "price": product["price"],
        "quantity": random.randint(1, 5)
    }


def send_order(order):
    response = requests.post(
        API_URL,
        json=order
    )
    if response.status_code == 200:
        # Fix — return order_id from our order
        # not from response!
        return order["order_id"]
    else:
        print(f"Error: {response.json()}")
        return None
   



def fetch_payment_status(order_id):
    # Simulate payment statuses
    statuses = [
        "completed",
        "pending", 
        "failed",
        "refunded"
    ]
    
    # Randomly assign a payment status
    # In real world this would call Stripe API:
    # response = requests.get(
    #     f"https://api.stripe.com/v1/charges/{order_id}",
    #     headers={"Authorization": f"Bearer {STRIPE_API_KEY}"}
    # )
    
    return {
        "order_id": order_id,
        "status": random.choice(statuses),
        "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}"
    }

# ─── Main ───
if __name__ == "__main__":
    for i in range(TOTAL_ORDERS):
        order = generate_order()
        order_id = send_order(order)
        
        # Show progress every 100 orders
        if i % 100 == 0:
            print(f"Progress: {i}/{TOTAL_ORDERS} orders sent")   
        
        