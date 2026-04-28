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

CUSTOMERS_DATA = [
    {"id": 1, "name": "John Smith", "address": "London", "tier": "Standard"},
    {"id": 2, "name": "Jane Doe", "address": "Manchester", "tier": "Premium"},
    {"id": 3, "name": "Bob Johnson", "address": "Birmingham", "tier": "Standard"},
    {"id": 4, "name": "Alice Brown", "address": "Leeds", "tier": "VIP"},
    {"id": 5, "name": "Charlie Wilson", "address": "Edinburgh", "tier": "Premium"},
]

# ─── Functions ───
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

def send_order(order):
    response = requests.post(API_URL, json=order)
    if response.status_code == 200:
        return order["order_id"]
    else:
        print(f"Error: {response.json()}")
        return None

def generate_customer():
    customer = random.choice(CUSTOMERS_DATA)
    return {
        "customer_id": f"CUST-{customer['id']:03d}",
        "name": customer["name"],
        "address": customer["address"],
        "tier": customer["tier"],
        "email": f"{customer['name'].lower().replace(' ', '.')}@gmail.com",
        "phone": f"07{random.randint(100000000, 999999999)}",
        "updated_at": datetime.now().isoformat()
    }

def send_customer(customer):
    response = requests.post(CUSTOMER_API_URL, json=customer)
    if response.status_code == 200:
        return customer["customer_id"]
    else:
        print(f"Error: {response.json()}")
        return None

def fetch_payment_status(order_id):
    statuses = ["completed", "pending", "failed", "refunded"]
    return {
        "order_id": order_id,
        "status": random.choice(statuses),
        "transaction_id": f"TXN-{uuid.uuid4().hex[:8].upper()}"
    }

# ─── Main ───
if __name__ == "__main__":
    # Send orders in batches of 1000
    batch = []
    for i in range(TOTAL_ORDERS):
        order = generate_order()
        batch.append(order)
        if len(batch) == 1000:
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket='ecommerce-data-platform-dev-raw',
                Key=f"orders/batch_{uuid.uuid4().hex[:8]}.json",
                Body=json.dumps(batch)
            )
            print(f"Saved batch of 1000 orders! Total: {i+1}")
            batch = []

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