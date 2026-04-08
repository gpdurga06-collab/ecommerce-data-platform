from spark_jobs.utils.spark_session import create_spark_session
import pyspark.sql.functions as F


def transform_orders():
    # Create Spark session
    spark = create_spark_session()


    # Define the S3 path (using s3a protocol)
    s3_bucket_path = "s3a://ecommerce-data-platform-dev-raw/orders/ORD-001.json"

    # Read JSON data from S3 into a DataFrame
    df = spark.read.json(s3_bucket_path)

    # Show data
    df.show()

    # Data cleaning and transformation

    df_clean = df.dropDuplicates().na.drop().withColumn("total", df.price * df.quantity)

    # Show cleaned data
    df_clean.show()


    # parquet # Write the DataFrame to S3 in Parquet format
    output_path = "s3a://ecommerce-data-platform-dev-processed/orders/ORD-001.parquet"
    df_clean.write.mode("overwrite").parquet(output_path)

