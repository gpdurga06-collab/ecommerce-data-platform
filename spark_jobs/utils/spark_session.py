from pyspark.sql import SparkSession


def create_spark_session():
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("ecommerce-data-platform")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
        )
        .getOrCreate()
    )
    return spark
