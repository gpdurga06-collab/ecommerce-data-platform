from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("ecommerce-business-logic") \
    .getOrCreate()

# Read from processed zone
df = spark.read.parquet(
    "s3://ecommerce-data-platform-dev-processed/orders/"
)

print(f"Total orders: {df.count()}")

# Revenue by customer
df.groupBy("customer_id") \
    .agg(F.sum("total").alias("total_revenue")) \
    .orderBy(F.desc("total_revenue")) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-curated/revenue/")

# Top products
df.groupBy("product") \
    .agg(F.sum("total").alias("total_revenue")) \
    .orderBy(F.desc("total_revenue")) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-curated/top_products/")

# Suspicious orders
df.withColumn("is_suspicious",
    F.when(F.col("total") > 10000, True).otherwise(False)) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-curated/suspicious_orders/")

print("Business logic complete! ✅")