from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("ecommerce-business-logic") \
    .getOrCreate()

# Read with mergeSchema for schema evolution!
df = spark.read \
    .option("mergeSchema", "true") \
    .parquet(
        "s3://ecommerce-data-platform-dev-processed/orders/"
    )

print(f"Total orders: {df.count()}")
print("Schema:")
df.printSchema()

# Repartition for better performance!
df_partitioned = df.repartition(10, "customer_id")
df_partitioned.cache()

# Revenue by customer
df_partitioned.groupBy("customer_id") \
    .agg(F.sum("total").alias("total_revenue")) \
    .orderBy(F.desc("total_revenue")) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-curated/revenue/")

print("Revenue written! ✅")

# Top products
df_partitioned.groupBy("product") \
    .agg(F.sum("total").alias("total_revenue")) \
    .orderBy(F.desc("total_revenue")) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-curated/top_products/")

print("Top products written! ✅")

# Suspicious orders
df_partitioned.withColumn("is_suspicious",
    F.when(F.col("total") > 10000, True).otherwise(False)) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save(
        "s3://ecommerce-data-platform-dev-curated/suspicious_orders/"
    )

print("Suspicious orders written! ✅")

# Discount analysis — new column!
df_partitioned.groupBy("product") \
    .agg(
        F.avg("discount_percentage").alias("avg_discount"),
        F.count("order_id").alias("total_orders")
    ) \
    .orderBy(F.desc("avg_discount")) \
    .write.format("parquet") \
    .mode("overwrite") \
    .save(
        "s3://ecommerce-data-platform-dev-curated/discount_analysis/"
    )

print("Discount analysis written! ✅")

df_partitioned.unpersist()
print("Business logic complete! ✅")