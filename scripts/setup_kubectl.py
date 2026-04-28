import subprocess
import boto3

eks = boto3.client('eks', region_name='us-east-2')
clusters = eks.list_clusters()

if not clusters['clusters']:
    print("No EKS clusters found! Skipping kubectl setup.")
else:
    cluster_name = clusters['clusters'][0]
    print(f"Updating kubeconfig for: {cluster_name}")
    result = subprocess.run([
        'aws', 'eks', 'update-kubeconfig',
        '--name', cluster_name,
        '--region', 'us-east-2'
    ], capture_output=True, text=True)
    print(result.stdout)
    print("kubectl configured!")