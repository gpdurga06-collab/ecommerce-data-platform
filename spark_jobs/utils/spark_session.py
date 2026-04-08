from pyspark.sql import SparkSession

def create_spark_session():
    spark = (
    SparkSession.builder
        .master("local[*]")
        .appName("ecommerce-data-platform")
        .config("spark.hadoop.fs.s3a.impl", 
        "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
        .getOrCreate()
)
    return spark

# Create a SparkSession
spark = SparkSession.builder \
    .appName("ReadDataFromS3") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1") \
    .getOrCreate()

# Define the S3 path (using s3a protocol)
s3_bucket_path = "s3://ecommerce-data-platform-dev-raw/orders/ORD-001.json"


# Read JSON data from S3 into a DataFrame
df = spark.read.json(s3_bucket_path)

# Show data
df.show()