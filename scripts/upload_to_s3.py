import boto3
import os
import zipfile
import subprocess
subprocess.run(['python', 'scripts/setup_kubectl.py'])

s3 = boto3.client('s3', region_name='us-east-2')
bucket = 'ecommerce-data-platform-dev-raw'

# Create dependencies.zip first
print("Creating dependencies.zip...")
with zipfile.ZipFile('dependencies.zip', 'w') as z:
    for root, dirs, files in os.walk('spark_jobs'):
        for file in files:
            z.write(os.path.join(root, file))
print("dependencies.zip created!")

# Files to upload
files = {
    'spark_jobs/transformations/business_logic_emr.py': 
        'scripts/business_logic_emr.py',
    'glue_script.py': 
        'scripts/glue_job_script.py',
    'dependencies.zip':
        'scripts/dependencies.zip',
}

for local_path, s3_key in files.items():
    s3.upload_file(local_path, bucket, s3_key)
    print(f"Uploaded {local_path} to s3://{bucket}/{s3_key}")

print("All files uploaded!")