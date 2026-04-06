import json
import boto3
import os
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    try:
        # Step 1 — Read incoming order data from API
        body = json.loads(event['body'])
        
        # Step 2 — Get bucket name from environment
        bucket_name = os.environ['BUCKET_NAME']
        
        # Step 3 — Validate order data
        if 'order_id' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Missing order_id!'
                })
            }
        
        logger.info(f"Processing order: {body['order_id']}")
        
        # Step 4 — Save order to S3
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"orders/{body['order_id']}.json",
            Body=json.dumps(body)
        )
        
        logger.info(f"Order {body['order_id']} saved to S3!")
        
        # Step 5 — Return success
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order saved successfully!',
                'order_id': body['order_id']
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error: {str(e)}'
            })
        }
