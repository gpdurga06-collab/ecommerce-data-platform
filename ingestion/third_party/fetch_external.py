# imports
# Correct — need the whole module
import random
import uuid
import requests
from datetime import datetime
import boto3
import json

API_URL = "http://localhost:8000/orders"
CUSTOMER_API_URL = "http://localhost:8000/customers"
TOTAL_ORDERS = 100000
TOTAL_CUSTOMERS = 30000

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


#Customer data to generate
CUSTOMERS_DATA = [
    {"id": 1, "name": "John Smith", "address": "London", "tier": "Standard"},
    {"id": 2, "name": "Jane Doe", "address": "Manchester", "tier": "Premium"},
    {"id": 3, "name": "Bob Johnson", "address": "Birmingham", "tier": "Standard"},
    {"id": 4, "name": "Alice Brown", "address": "Leeds", "tier": "VIP"},
    {"id": 5, "name": "Charlie Wilson", "address": "Edinburgh", "tier": "Premium"},
]

# Function to generate customer
def generate_order():
    product = random.choice(PRODUCTS)
    customer = random.choice(CUSTOMERS)
    return {
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "customer_id": f"CUST-{customer['id']:03d}",
        "product": product["name"],
        "price": product["price"],
        "quantity": random.randint(1, 5),
        "discount_percentage": round(random.uniform(0, 20), 2),
        "payment_method": random.choice(["card", "paypal", "cash"])
    }

# Function to send customer
def send_customer(customer):
    response = requests.post(
        CUSTOMER_API_URL,
        json=customer
    )
    if response.status_code == 200:
        # Fix — return order_id from our order
        # not from response!
        return customer["customer_id"]
    else:
        print(f"Error: {response.json()}")
        return None
    


    
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

if __name__ == "__main__":
    # Send orders in batches of 1000
    batch = []
    for i in range(TOTAL_ORDERS):
        order = generate_order()
        batch.append(order)
        
        # When batch reaches 1000 → save to S3
        if len(batch) == 1000:
            # Save batch as one file
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket='ecommerce-data-platform-dev-raw',
                Key=f"orders/batch_{uuid.uuid4().hex[:8]}.json",
                Body=json.dumps(batch)
            )
            print(f"Saved batch of 1000 orders! Total: {i+1}")
            batch = []  # reset batch!

    # Send customers in batches of 1000
    batch = []
    for i in range(TOTAL_CUSTOMERS):
        customer = generate_customer()
        batch.append(customer)
        
        if len(batch) == 1000:
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket='ecommerce-data-platform-dev-raw',
                Key=f"customers/batch_{uuid.uuid4().hex[:8]}.json",
                Body=json.dumps(batch)
            )
            print(f"Saved batch of 1000 customers! Total: {i+1}")
            batch = []