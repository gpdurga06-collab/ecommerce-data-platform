from fastapi import FastAPI
from pydantic import BaseModel
import boto3
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(
    title="E-Commerce Data Platform API",
    description="REST API for ingesting order data",
    version="1.0.0"
)

class Order(BaseModel):
    order_id: str
    customer_id: str
    product: str
    price: float
    quantity: int

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "ecommerce-api"
    }
@app.post("/orders")
def create_order(order: Order):
    try:
        bucket_name = os.environ.get('BUCKET_NAME', 'local-bucket')
        
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=bucket_name,
            Key=f"orders/{order.order_id}.json",
            Body=json.dumps(order.dict())
        )
        
        logger.info(f"Order {order.order_id} saved!")
        
        return {
            "status": "success",
            "message": f"Order {order.order_id} saved!",
            "order_id": order.order_id
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }