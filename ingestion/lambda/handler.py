import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')
        sfn_client = boto3.client('stepfunctions')
        state_machine_arn = os.environ.get('STATE_MACHINE_ARN')
        
        # Handle S3 event trigger
        if 'Records' in event:
            record = event['Records'][0]
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            logger.info(f"New file: s3://{bucket}/{key}")
            
            # Read batch file
            response = s3_client.get_object(
                Bucket=bucket,
                Key=key
            )
            content = response['Body'].read().decode('utf-8')
            orders = json.loads(content)
            
            logger.info(f"Found {len(orders)} orders")
            
            # Validate orders
            valid = [o for o in orders 
                    if 'order_id' in o and 'price' in o]
            
            logger.info(f"Valid orders: {len(valid)}")
            
        else:
            logger.info("Manual trigger!")

        # Trigger Step Functions
        sfn_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps({
                "source": "lambda",
                "status": "validated"
            })
        )
        
        logger.info("Step Functions triggered! ✅")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Pipeline triggered!')
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise e
