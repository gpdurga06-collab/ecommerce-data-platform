# Run this Python script first
python -c "
import boto3
s3 = boto3.resource('s3')
buckets = [
    'ecommerce-data-platform-dev-raw',
    'ecommerce-data-platform-dev-processed',
    'ecommerce-data-platform-dev-curated'
]
for bucket_name in buckets:
    try:
        bucket = s3.Bucket(bucket_name)
        bucket.object_versions.delete()
        print(f'Emptied {bucket_name}')
    except Exception as e:
        print(f'Error: {e}')
"