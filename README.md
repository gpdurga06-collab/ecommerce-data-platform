# ecommerce-data-platform
End to end data engineering project using PySpark, AWS, Databricks, Terraform, Docker and Kubernetes
# E-Commerce Data Platform

## 📋 Overview
## 🏗️ Architecture
## 🛠️ Tech Stack
## 📁 Project Structure
## 🚀 How to Run
## 📊 Data Pipeline Flow
## 🔧 Infrastructure
## 📈 Monitoring
## 🧪 Testing
## 👨‍💻 Author


# 🛒 E-Commerce Data Platform

A production-grade, end-to-end data engineering platform built on AWS and Databricks, processing 100,000+ orders through a fully automated Medallion Architecture pipeline.

---

## 📋 Overview

This project demonstrates a complete data engineering solution for an e-commerce business. It ingests order and customer data through a REST API, processes it through a multi-layer pipeline using AWS services, and delivers analytics-ready Delta tables in Databricks with full monitoring and CI/CD automation.

**Key capabilities:**
- Ingests 100,000+ orders and 30,000+ customer records
- Processes data through Bronze → Silver → Gold Medallion Architecture
- Tracks customer history using SCD Type 2
- Deploys containerized API to AWS EKS via automated CI/CD
- Monitors pipeline health with AWS CloudWatch
- Delivers business insights through Databricks Analytics Dashboard

---

## 🏗️ Architecture

```
REST API (FastAPI/Docker/Kubernetes)
        ↓
AWS Lambda (validate + trigger)
        ↓
AWS Step Functions (orchestrate)
        ↓
┌─────────────────────────────────┐
│         AWS S3 Data Lake        │
│  Raw → Processed → Curated      │
└─────────────────────────────────┘
        ↓
Glue Crawler → Glue ETL → EMR PySpark
        ↓
Databricks (Unity Catalog → Delta Lake)
        ↓
┌─────────────────────────────────┐
│     Delta Live Tables           │
│  Bronze → Silver → Gold         │
│  + SCD2 Customer Dimension      │
└─────────────────────────────────┘
        ↓
Analytics Dashboard + CloudWatch Monitoring
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **Languages** | Python, SQL, HCL (Terraform), YAML |
| **Ingestion** | FastAPI, AWS Lambda, REST APIs |
| **Storage** | AWS S3 (Medallion Architecture), Delta Lake |
| **Processing** | PySpark, AWS EMR, AWS Glue ETL |
| **Cataloguing** | AWS Glue Crawler, Glue Data Catalog, Unity Catalog |
| **Orchestration** | AWS Step Functions, Databricks Delta Live Tables |
| **Analytics** | Databricks, Delta Tables, SCD Type 2 |
| **Infrastructure** | Terraform, AWS IAM, AWS VPC |
| **Containers** | Docker, Kubernetes, AWS EKS |
| **CI/CD** | GitHub Actions |
| **Monitoring** | AWS CloudWatch, Databricks Dashboard |
| **Testing** | pytest, PySpark unit tests |
| **Governance** | Unity Catalog, Delta Lake ACID |

---

## 📁 Project Structure

```
ecommerce-data-platform/
│
├── ingestion/
│   ├── api/
│   │   └── app.py                    # FastAPI REST API
│   ├── lambda/
│   │   ├── handler.py                # AWS Lambda function
│   │   └── handler.zip               # Packaged Lambda
│   └── third_party/
│       └── fetch_external.py         # Data generator + CRM fetcher
│
├── spark_jobs/
│   ├── utils/
│   │   └── spark_session.py          # Reusable SparkSession
│   └── transformations/
│       ├── orders_transform.py       # Clean and transform orders
│       └── business_logic.py        # Revenue, rankings, fraud detection
│
├── databricks/
│   └── my_transformation.py          # Delta Live Tables pipeline
│
├── terraform/
│   ├── main.tf                       # AWS provider config
│   ├── variables.tf                  # Input variables
│   ├── outputs.tf                    # Output values
│   ├── s3.tf                         # S3 buckets (raw/processed/curated)
│   ├── iam.tf                        # IAM roles and policies
│   ├── glue.tf                       # Glue crawler and ETL job
│   ├── lambda.tf                     # Lambda function
│   ├── emr.tf                        # EMR cluster
│   ├── step_functions.tf             # Step Functions pipeline
│   ├── eks.tf                        # EKS cluster and node group
│   └── cloudwatch.tf                 # Monitoring dashboard and alarms
│
├── kubernetes/
│   ├── deployment.yaml               # K8s deployment (2 replicas)
│   └── service.yaml                  # K8s NodePort service
│
├── docker/
│   ├── Dockerfile.api                # API container
│   └── Dockerfile.spark              # PySpark container
│
├── tests/
│   ├── test_business_logic.py        # PySpark unit tests
│   └── test_orders_transform.py      # Transformation tests
│
├── .github/
│   └── workflows/
│       └── ci_cd.yml                 # GitHub Actions pipeline
│
└── README.md
```

---

## 🔄 Data Pipeline Flow

### Step 1 — Data Ingestion:
```
fetch_external.py generates orders and customer data
        ↓
POST /orders → FastAPI validates → S3 raw zone
POST /customers → FastAPI validates → S3 raw zone
        ↓
Batch files (1000 records per file) ← avoids small file problem!
```

### Step 2 — AWS Pipeline:
```
Lambda validates incoming data
        ↓
Step Functions orchestrates:
  → Glue Crawler scans S3 raw zone
  → Updates Glue Data Catalog
  → Glue ETL cleans data → S3 processed zone
  → EMR PySpark applies business logic:
      → Revenue per customer
      → Top selling products
      → Suspicious order detection
  → Results saved to S3 curated zone
```

### Step 3 — Databricks Analytics:
```
Unity Catalog connects to S3 via IAM role
        ↓
Delta Live Tables pipeline runs automatically:
  → Bronze: raw orders and customers from S3
  → Silver: cleaned data with quality checks
  → Gold: revenue metrics and rankings
  → dim_customer: SCD2 customer history
        ↓
Databricks Dashboard shows business insights
```

---

## 🚀 How to Run

### Prerequisites:
- Python 3.11+
- Java 11+
- AWS CLI configured
- Terraform 1.6+
- Docker Desktop
- kubectl

### 1. Clone the repository:
```bash
git clone https://github.com/gpdurga06-collab/ecommerce-data-platform.git
cd ecommerce-data-platform
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Provision AWS infrastructure:
```bash
cd terraform
terraform init
terraform apply
```

### 4. Start the API:
```bash
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e AWS_DEFAULT_REGION=us-east-2 \
  -e BUCKET_NAME=ecommerce-data-platform-dev-raw \
  gpdurga06093/ecommerce-api:latest
```

### 5. Generate data:
```bash
python ingestion/third_party/fetch_external.py
```

### 6. Run tests:
```bash
pytest tests/ -v
```

### 7. Deploy to Kubernetes:
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get pods
```

---

## 🏛️ Medallion Architecture

| Layer | Location | Description |
|---|---|---|
| **Bronze** | S3 raw + Delta | Raw data as received — never modified |
| **Silver** | S3 processed + Delta | Cleaned, validated, deduplicated |
| **Gold** | S3 curated + Delta | Business metrics and aggregations |

---

## 📊 Delta Lake Features

| Feature | Implementation |
|---|---|
| **ACID Transactions** | All Delta table writes are atomic |
| **Time Travel** | Query any previous version of data |
| **Schema Evolution** | Add columns without rewriting data |
| **Schema Enforcement** | Reject data that doesn't match schema |
| **SCD Type 2** | Full customer history with start/end dates |

---

## 🔄 SCD Type 2 — Customer Dimension

Tracks complete history of customer changes:

```
customer_id  address     tier      start_date  end_date    is_current
CUST-001     London      Standard  2026-04-16  2026-04-18  false ← expired
CUST-001     Manchester  Premium   2026-04-18  9999-12-31  true  ← current
```

---

## 🔧 Infrastructure (Terraform)

All AWS infrastructure is provisioned as code:

| Resource | Purpose |
|---|---|
| S3 (3 buckets) | Raw, Processed, Curated data lake |
| Lambda | Data validation and pipeline trigger |
| Glue Crawler | Schema detection and catalog update |
| Glue ETL | Basic data cleaning and transformation |
| EMR | Heavy PySpark business logic processing |
| Step Functions | Pipeline orchestration |
| EKS | Production Kubernetes cluster |
| CloudWatch | Monitoring dashboard and alarms |
| IAM | Fine-grained security and permissions |

---

## 🚀 CI/CD Pipeline

GitHub Actions automatically runs on every push to main:

```
Push to GitHub
        ↓
Run pytest unit tests
        ↓
Build Docker image
        ↓
Push to Docker Hub
        ↓
Deploy to AWS EKS (if cluster running)
```

---

## 📈 Monitoring

### AWS CloudWatch Dashboard:
- Lambda invocations, errors and duration
- Step Functions execution success/failure
- Glue job performance metrics
- S3 storage growth over time
- Alarms for Lambda errors > 5 and pipeline failures

### Databricks Analytics Dashboard:
- Total orders processed (100K+)
- Total revenue ($6M+)
- Revenue by customer
- Top products by revenue
- Customer tier analysis

---

## 🧪 Testing

Unit tests cover all PySpark transformations:

```bash
pytest tests/test_business_logic.py -v
```

| Test | What it covers |
|---|---|
| `test_revenue_calculation` | price × quantity |
| `test_revenue_by_customer` | groupBy customer_id |
| `test_top_products` | orderBy revenue desc |
| `test_flag_suspicious_orders` | revenue > threshold |
| `test_data_cleaning` | dropDuplicates + na.drop |
| `test_total_calculation` | total column creation |

---

## 🌟 Key Achievements

- ✅ Processed 100,000 orders end to end
- ✅ Zero data loss with Delta Lake ACID guarantees
- ✅ Full customer history with SCD Type 2
- ✅ Automated CI/CD with zero manual deployments
- ✅ Production Kubernetes on AWS EKS
- ✅ Real time monitoring with CloudWatch
- ✅ Data quality enforcement with DLT expectations
- ✅ Infrastructure as Code with Terraform

---

## 👨‍💻 Author

**Phani Durga**
- GitHub: [@gpdurga06-collab](https://github.com/gpdurga06-collab)
- Project: [ecommerce-data-platform](https://github.com/gpdurga06-collab/ecommerce-data-platform)

---

*Built with ❤️ using AWS, Databricks, PySpark, Terraform, Docker and Kubernetes*