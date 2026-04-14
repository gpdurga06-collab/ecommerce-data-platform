import pytest
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
    yield spark
    spark.stop()


def test_transform_business_logic(spark):
    # Create a Spark session for testing
    # spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

    # Sample data for testing
    data = [
        {
            "customer_id": "CUST-001",
            "product": "Product A",
            "price": 100.0,
            "quantity": 2,
        },
        {
            "customer_id": "CUST-002",
            "product": "Product B",
            "price": 50.0,
            "quantity": 1,
        },
        {
            "customer_id": "CUST-001",
            "product": "Product C",
            "price": 200.0,
            "quantity": 1,
        },
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Perform the business logic transformation (revenue calculation)
    df = df.withColumn("revenue", df.price * df.quantity)

    # Collect the results for assertion
    results = df.select("customer_id", "product", "revenue").collect()

    # Assert the expected revenue values
    assert results[0]["revenue"] == 200.0  # CUST-001, Product A
    assert results[1]["revenue"] == 50.0  # CUST-002, Product B
    assert results[2]["revenue"] == 200.0  # CUST-001, Product C


def test_revenue_by_customer(spark):
    # Sample data for testing
    data = [
        {"customer_id": "CUST-001", "revenue": 300.0},
        {"customer_id": "CUST-002", "revenue": 50.0},
        {"customer_id": "CUST-001", "revenue": 200.0},
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Group by customer_id and calculate total revenue
    revenue_by_customer = (
        df.groupBy("customer_id")
        .agg(F.sum("revenue").alias("total_revenue"))
        .orderBy(F.desc("total_revenue"))
    )

    # Collect the results for assertion
    results = revenue_by_customer.collect()

    # Assert the expected total revenue values
    assert results[0]["total_revenue"] == 500.0  # CUST-001
    assert results[1]["total_revenue"] == 50.0  # CUST-002


def test_top_products(spark):
    # Sample data for testing
    data = [
        {"product": "Product A", "revenue": 300.0},
        {"product": "Product B", "revenue": 50.0},
        {"product": "Product C", "revenue": 200.0},
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Group by product and calculate total revenue, then order by revenue
    top_products = (
        df.groupBy("product")
        .agg(F.sum("revenue").alias("total_revenue"))
        .orderBy(F.desc("total_revenue"))
        .limit(10)
    )

    # Collect the results for assertion
    results = top_products.collect()

    # Assert the expected total revenue values
    assert results[0]["total_revenue"] == 300.0  # Product A
    assert results[1]["total_revenue"] == 200.0  # Product C
    assert results[2]["total_revenue"] == 50.0  # Product B


def test_flag_suspicious_orders(spark):
    # Sample data for testing
    data = [
        {"order_id": "ORD-001", "revenue": 5000.0},
        {"order_id": "ORD-002", "revenue": 15000.0},
        {"order_id": "ORD-003", "revenue": 8000.0},
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Flag suspicious orders based on revenue threshold
    df = df.withColumn(
        "is_suspicious", F.when(F.col("revenue") > 10000, True).otherwise(False)
    )

    # Collect the results for assertion
    results = df.select("order_id", "is_suspicious").collect()

    # Assert the expected suspicious order flags
    assert results[0]["is_suspicious"] == False  # ORD-001
    assert results[1]["is_suspicious"] == True  # ORD-002
    assert results[2]["is_suspicious"] == False  # ORD-003


def test_data_cleaning(spark):
    # Sample data for testing
    data = [
        {"order_id": "ORD-001", "price": 100.0, "quantity": 2},
        {"order_id": "ORD-002", "price": None, "quantity": 1},
        {"order_id": "ORD-001", "price": 100.0, "quantity": 2},  # Duplicate
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Perform data cleaning (drop duplicates and nulls)
    df_clean = df.dropDuplicates().na.drop()

    # Collect the results for assertion
    results = df_clean.select("order_id", "price", "quantity").collect()

    # Assert the expected cleaned data values
    assert len(results) == 1  # Only one unique, non-null record should remain
    assert results[0]["order_id"] == "ORD-001"
    assert results[0]["price"] == 100.0
    assert results[0]["quantity"] == 2


def test_total_calculation(spark):
    # Sample data for testing
    data = [
        {"order_id": "ORD-001", "price": 100.0, "quantity": 2},
        {"order_id": "ORD-002", "price": 50.0, "quantity": 1},
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Calculate total revenue for each order
    df = df.withColumn("total", df.price * df.quantity)

    # Collect the results for assertion
    results = df.select("order_id", "total").collect()

    # Assert the expected total values
    assert results[0]["total"] == 200.0  # ORD-001
    assert results[1]["total"] == 50.0  # ORD-002


def test_revenue_calculation(spark):

    # Sample data for testing
    data = [
        {
            "customer_id": "CUST-001",
            "product": "Product A",
            "price": 100.0,
            "quantity": 2,
        },
        {
            "customer_id": "CUST-002",
            "product": "Product B",
            "price": 50.0,
            "quantity": 1,
        },
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Calculate revenue for each order
    df = df.withColumn("revenue", df.price * df.quantity)

    # Collect the results for assertion
    results = df.select("customer_id", "product", "revenue").collect()

    # Assert the expected revenue values
    assert results[0]["revenue"] == 200.0  # CUST-001, Product A
    assert results[1]["revenue"] == 50.0  # CUST-002, Product B


def test_revenue_by_customer_calculation(spark):
    # Sample data for testing
    data = [
        {"customer_id": "CUST-001", "revenue": 300.0},
        {"customer_id": "CUST-002", "revenue": 50.0},
        {"customer_id": "CUST-001", "revenue": 200.0},
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Group by customer_id and calculate total revenue
    revenue_by_customer = (
        df.groupBy("customer_id")
        .agg(F.sum("revenue").alias("total_revenue"))
        .orderBy(F.desc("total_revenue"))
    )

    # Collect the results for assertion
    results = revenue_by_customer.collect()

    # Assert the expected total revenue values
    assert results[0]["total_revenue"] == 500.0  # CUST-001
    assert results[1]["total_revenue"] == 50.0  # CUST-002


def test_top_products_calculation(spark):
    # Sample data for testing
    data = [
        {"product": "Product A", "revenue": 300.0},
        {"product": "Product B", "revenue": 50.0},
        {"product": "Product C", "revenue": 200.0},
    ]

    # Create a DataFrame from the sample data
    df = spark.createDataFrame(data)

    # Group by product and calculate total revenue, then order by revenue
    top_products = (
        df.groupBy("product")
        .agg(F.sum("revenue").alias("total_revenue"))
        .orderBy(F.desc("total_revenue"))
        .limit(10)
    )

    # Collect the results for assertion
    results = top_products.collect()

    # Assert the expected total revenue values
    assert results[0]["total_revenue"] == 300.0  # Product A
    assert results[1]["total_revenue"] == 200.0  # Product C
    assert results[2]["total_revenue"] == 50.0  # Product B
