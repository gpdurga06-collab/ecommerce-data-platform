from spark_jobs.utils.spark_session import create_spark_session
import pyspark.sql.functions as F

def transform_business_logic():
    # Create Spark session
    spark = create_spark_session()

    # Define the S3 path (using s3a protocol)
    s3_bucket_path = "s3a://ecommerce-data-platform-dev-processed/orders/ORD-001.parquet"

    # Read Parquet data from S3 into a DataFrame
    df = spark.read.parquet(s3_bucket_path)

    # Show data
    df.show()

    # revenue calculation    
    df = df.withColumn("revenue", F.col("price") * F.col("quantity"))
    
    df.show()
    
    
    # write revenue data back to S3    
    output_path = "s3a://ecommerce-data-platform-dev-curated/revenue/REV-001.parquet"
    df.write.mode("overwrite").parquet(output_path)
    
    
    # top 10 products by revenue
    top_products = df.groupBy("product_id").agg(F.sum("revenue").alias("total_revenue")).orderBy(
        F.desc("total_revenue")
    ).limit(10)
    top_products.show()
    
    # write top products data back to S3
    output_path = "s3a://ecommerce-data-platform-dev-curated/top_products/TOP-001.parquet"
    top_products.write.mode("overwrite").parquet(output_path)
    
    #flag suspicious orders
    df = df.withColumn("is_suspicious", F.when(F.col("revenue") > 1000, True).otherwise(False))
    df.show()
    
    # write suspicious orders data back to S3
    output_path = "s3a://ecommerce-data-platform-dev-curated/suspicious_orders/SUS-001.parquet"
    df.write.mode("overwrite").parquet(output_path)

