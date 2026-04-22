from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("ecommerce-glue-etl") \
    .getOrCreate()

df = spark.read.json(
    "s3://ecommerce-data-platform-dev-raw/orders/"
)
print(f"Total raw orders: {df.count()}")

df_clean = df.dropDuplicates() \
             .na.drop() \
             .withColumn("total",
                F.col("price") * F.col("quantity"))

print(f"Total clean orders: {df_clean.count()}")

df_clean.write \
    .format("parquet") \
    .mode("overwrite") \
    .save("s3://ecommerce-data-platform-dev-processed/orders/")

print("Done! ✅")
