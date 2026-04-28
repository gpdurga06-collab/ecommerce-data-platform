from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("ecommerce-glue-etl") \
    .getOrCreate()

# Read ALL orders including new schema!
df = spark.read \
    .option("mergeSchema", "true") \
    .json("s3://ecommerce-data-platform-dev-raw/orders/")

print(f"Total raw orders: {df.count()}")
print("Schema:")
df.printSchema()

# Clean data — only drop rows missing critical fields
df_clean = df.dropDuplicates() \
             .na.drop(subset=["order_id", "price"]) \
             .withColumn("total",
                F.col("price") * F.col("quantity"))

print(f"Total clean orders: {df_clean.count()}")

# Write with mergeSchema to handle schema evolution!
df_clean.write \
    .format("parquet") \
    .option("mergeSchema", "true") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-processed/orders/")

print("Schema evolution handled! Done! ✅")