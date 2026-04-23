import subprocess
import boto3

# Get EKS cluster name
eks = boto3.client('eks', region_name='us-east-2')
clusters = eks.list_clusters()
cluster_name = clusters['clusters'][0]

print(f"Updating kubeconfig for: {cluster_name}")

# Update kubeconfig
result = subprocess.run([
    'aws', 'eks', 'update-kubeconfig',
    '--name', cluster_name,
    '--region', 'us-east-2'
], capture_output=True, text=True)

print(result.stdout)
print("kubectl configured! ✅")

# Verify
result = subprocess.run(
    ['kubectl', 'get', 'nodes'],
    capture_output=True, text=True
)
print(result.stdout)