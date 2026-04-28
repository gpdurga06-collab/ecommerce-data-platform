from fastapi import FastAPI
from pydantic import BaseModel
import boto3
import json
import os

app = FastAPI(
    title="E-Commerce Data Platform API",
    description="REST API for ingesting order and CRM data",
    version="1.0.0"
)

class Order(BaseModel):
    order_id: str
    customer_id: str
    product: str
    price: float
    quantity: int
    discount_percentage: float = 0.0
    payment_method: str = "card"

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    address: str
    tier: str
    phone: str
    updated_at: str

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "ecommerce-api"
    }

@app.post("/orders")
def create_order(order: Order):
    try:
        bucket_name = os.environ.get('BUCKET_NAME')
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=bucket_name,
            Key=f"orders/{order.order_id}.json",
            Body=json.dumps(order.dict())
        )
        return {
            "status": "success",
            "message": f"Order {order.order_id} saved!",
            "order_id": order.order_id
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/customers")
def create_customer(customer: Customer):
    try:
        bucket_name = os.environ.get('BUCKET_NAME')
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=bucket_name,
            Key=f"customers/{customer.customer_id}.json",
            Body=json.dumps(customer.dict())
        )
        return {
            "status": "success",
            "message": f"Customer {customer.customer_id} saved!",
            "customer_id": customer.customer_id
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}