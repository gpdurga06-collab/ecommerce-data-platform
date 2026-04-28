# 🛒 E-Commerce Data Platform

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-%23FF3621.svg?style=for-the-badge&logo=databricks&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=for-the-badge&logo=apachespark&logoColor=black)
![Terraform](https://img.shields.io/badge/Terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-%23003366.svg?style=for-the-badge&logo=delta&logoColor=white)

> A **production-grade, end-to-end data engineering platform** built on AWS and Databricks, processing **200,000+ orders** through a fully automated Medallion Architecture pipeline with real-time monitoring, SCD Type 2, and schema evolution support.

---

## 📊 Project Stats

| Metric | Value |
|---|---|
| Total Orders Processed | 200,000+ |
| Total Revenue Generated | $6M+ |
| AWS Resources (Terraform) | 47 |
| Pipeline Execution Time | ~4 minutes |
| Data Layers | Bronze → Silver → Gold |
| Test Coverage | 6 unit tests |
| CI/CD | Fully automated |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA INGESTION                          │
│                                                             │
│   fetch_external.py → FastAPI (Docker) → AWS EKS           │
│         ↓                    ↓                              │
│   Batch Files (1000/file)   REST API (/orders /customers)   │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   AWS S3 RAW ZONE                           │
│              (Medallion Architecture Layer 1)               │
│         orders/batch_*.json  customers/batch_*.json         │
└──────────┬──────────────────────────────────────────────────┘
           ↓ S3 Event Notification
┌─────────────────────────────────────────────────────────────┐
│                   AWS LAMBDA                                │
│         Validates batch → Checks duplicates                 │
│         Triggers Step Functions                             │
└──────────┬──────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────────┐
│              AWS STEP FUNCTIONS PIPELINE                    │
│                                                             │
│   StartCrawler → RunGlueJob → RunEMR                        │
│        ↓              ↓           ↓                         │
│   Glue Crawler   Glue ETL    EMR PySpark                    │
│   (scan S3)   (clean data)  (business logic)                │
└──────────┬──────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────────────────────────────────────┐
│              S3 PROCESSED + CURATED ZONES                    │
│                                                              │
│   processed/orders/*.parquet   curated/revenue/*.parquet     │
│                                curated/top_products/         │
│                                curated/suspicious_orders/    │
│                                curated/discount_analysis/    │
└──────────┬───────────────────────────────────────────────────┘
           ↓ Unity Catalog
┌──────────────────────────────────────────────────────────────┐
│              DATABRICKS DELTA LIVE TABLES                    │
│                                                              │
│   Bronze (raw) → Silver (clean) → Gold (metrics)            │
│        ↓                                                     │
│   dim_customer (SCD Type 2)                                  │
│   Schema Evolution (mergeSchema)                             │
└──────────┬───────────────────────────────────────────────────┘
           ↓
┌──────────────────────────────────────────────────────────────┐
│         ANALYTICS + MONITORING                               │
│                                                              │
│   Databricks Dashboard    AWS CloudWatch Dashboard           │
│   (Business metrics)      (Pipeline health)                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Languages** | Python 3.11, SQL, HCL (Terraform), YAML |
| **Ingestion** | FastAPI, AWS Lambda, REST API |
| **Storage** | AWS S3, Delta Lake, Parquet |
| **Processing** | PySpark, AWS EMR, AWS Glue ETL |
| **Orchestration** | AWS Step Functions, EventBridge, DLT |
| **Cataloguing** | AWS Glue Catalog, Databricks Unity Catalog |
| **Analytics** | Databricks, Delta Tables, SCD Type 2 |
| **Infrastructure** | Terraform, AWS IAM, VPC |
| **Containers** | Docker, Kubernetes, AWS EKS |
| **CI/CD** | GitHub Actions |
| **Monitoring** | AWS CloudWatch, Databricks Dashboard |
| **Testing** | pytest, PySpark unit tests |

---

## 🚀 Key Features

### ✅ Fully Automated Pipeline
New data landing in S3 automatically triggers the entire pipeline without human intervention — from Lambda validation through Glue ETL to EMR processing.

### ✅ Medallion Architecture
Three-layer data architecture (Bronze → Silver → Gold) ensuring data quality, traceability and business-ready analytics at every stage.

### ✅ SCD Type 2
Complete customer history tracking using Databricks Delta Live Tables `apply_changes` with full audit trail of all customer updates.

### ✅ Schema Evolution
Seamless handling of schema changes using PySpark `mergeSchema` — old records get NULL for new columns, new records have actual values. Zero pipeline downtime.

### ✅ Infrastructure as Code
All 47 AWS resources defined in Terraform — fully reproducible, version controlled and deployable in minutes.

### ✅ Production Kubernetes
Containerized FastAPI deployed to AWS EKS with 2 replicas, auto-restart on failure and rolling updates via CI/CD.

### ✅ Real-time Monitoring
AWS CloudWatch dashboard tracking Lambda invocations, Step Functions executions, Glue job duration and S3 storage metrics with automated alarms.

---

## 📁 Project Structure

```
ecommerce-data-platform/
│
├── ingestion/
│   ├── api/app.py                    # FastAPI REST API
│   ├── lambda/handler.py             # AWS Lambda function
│   └── third_party/fetch_external.py # Data generator
│
├── spark_jobs/
│   ├── utils/spark_session.py        # Reusable SparkSession
│   └── transformations/
│       ├── orders_transform.py       # Order transformations
│       ├── business_logic.py         # Business logic
│       └── business_logic_emr.py     # EMR optimized PySpark
│
├── databricks/
│   └── my_transformation.py          # Delta Live Tables pipeline
│
├── terraform/
│   ├── main.tf                       # AWS provider
│   ├── variables.tf                  # Variables
│   ├── s3.tf                         # S3 buckets
│   ├── iam.tf                        # IAM roles
│   ├── glue.tf                       # Glue crawler + ETL
│   ├── lambda.tf                     # Lambda function
│   ├── emr.tf                        # EMR cluster
│   ├── step_functions.tf             # Pipeline orchestration
│   ├── eks.tf                        # Kubernetes cluster
│   ├── eventbridge.tf                # Event automation
│   └── cloudwatch.tf                 # Monitoring
│
├── kubernetes/
│   ├── deployment.yaml               # K8s deployment
│   └── service.yaml                  # K8s service
│
├── docker/
│   ├── Dockerfile.api                # API container
│   └── Dockerfile.spark              # Spark container
│
├── scripts/
│   ├── upload_to_s3.py               # S3 upload utility
│   └── setup_kubectl.py              # kubectl configuration
│
├── tests/
│   └── test_business_logic.py        # PySpark unit tests
│
├── glue_script.py                    # Standalone Glue ETL
├── .github/workflows/ci_cd.yml       # GitHub Actions
└── README.md
```

---

## 🔄 Data Pipeline Flow

```
Step 1 — Ingestion:
fetch_external.py generates 200,000 orders
→ Saves in batches of 1,000 to S3 raw zone
→ Avoids small file problem! ✅

Step 2 — Event Trigger:
New file in S3 orders/ folder
→ S3 notification → Lambda
→ Lambda validates batch orders
→ Checks no duplicate pipeline running
→ Triggers Step Functions! ✅

Step 3 — AWS Pipeline:
Step Functions orchestrates:
→ Glue Crawler scans ALL S3 files
→ Updates Glue Data Catalog
→ Glue ETL cleans data (mergeSchema)
→ Writes Parquet to processed zone
→ EMR PySpark applies business logic:
   → Revenue by customer
   → Top selling products
   → Suspicious order detection
   → Discount analysis
→ Results to curated zone ✅

Step 4 — Databricks Analytics:
DLT pipeline (scheduled daily at 2am):
→ Bronze: raw orders + customers from S3
→ Silver: cleaned with quality checks
→ Gold: revenue metrics and rankings
→ dim_customer: SCD2 history ✅
```

---

## 📊 Schema Evolution Demo

One of the key features of this project is demonstrating schema evolution in a production pipeline.

**Old schema (100,000 orders):**
```
order_id, customer_id, product, price, quantity
```

**New schema (100,000 orders):**
```
order_id, customer_id, product, price, quantity,
discount_percentage, payment_method
```

**Result in Delta table:**
```
Old orders → discount_percentage = NULL ✅
New orders → discount_percentage = 15.0 ✅
Zero data loss! Zero pipeline changes! ✅
```

---

## 🔄 SCD Type 2 Demo

```
customer_id | address    | tier     | is_current
CUST-001    | London     | Standard | false  ← expired
CUST-001    | Manchester | Premium  | true   ← current
```

Full customer history preserved automatically using Databricks Delta Live Tables `apply_changes` with `stored_as_scd_type=2`.

---

## 🏛️ Medallion Architecture

| Layer | Location | Records | Purpose |
|---|---|---|---|
| **Bronze** | S3 raw + Delta | 200,001 | Raw as received |
| **Silver** | S3 processed + Delta | 200,001 | Cleaned + validated |
| **Gold** | S3 curated + Delta | 3 | Business metrics |
| **dim_customer** | Delta (SCD2) | 951 | Customer history |

---

## 🚀 How to Run

### Prerequisites:
- Python 3.11+, Java 11+, AWS CLI, Terraform 1.6+, Docker, kubectl

### Quick Start:
```bash
git clone https://github.com/gpdurga06-collab/ecommerce-data-platform.git
cd ecommerce-data-platform
pip install -r requirements.txt
cd terraform && terraform init && terraform apply
python scripts/upload_to_s3.py
python ingestion/third_party/fetch_external.py
pytest tests/ -v
```

---

## 💡 Real-World Challenges Solved

**Small File Problem** — Batch saving 1,000 records per file reduced S3 API calls by 1,000x.

**Duplicate Pipeline Executions** — Lambda checks if Step Functions is already running before triggering a new execution.

**EMR Credentials** — EMR EC2 nodes need both `elasticmapreduce.amazonaws.com` AND `ec2.amazonaws.com` in IAM trust policy.

**Schema Evolution** — PySpark `mergeSchema` allows old and new data to coexist with NULL values for missing columns in historical records.

---

## 🌟 Key Achievements

| Achievement | Detail |
|---|---|
| Processed 200K orders | End to end automated |
| Zero data loss | Delta Lake ACID guarantees |
| Schema evolution | No pipeline downtime |
| SCD Type 2 | Full customer history |
| 47 AWS resources | Fully as code |
| Auto CI/CD | Push to deploy |
| Real monitoring | CloudWatch + Databricks |

---

## 🗓️ Learning Roadmap

```
Phase 1 — E-Commerce Data Platform ✅ COMPLETE
Phase 2 — Python Deep Dive (May 2026)
Phase 3 — Terraform Deep Dive (Jun 2026)
Phase 4 — REST API + Lambda (Jun 2026)
Phase 5 — Docker + Kubernetes (Jul 2026)
Phase 6 — PySpark Deep Dive (Aug 2026)
Phase 7 — Databricks Complete (Aug 2026)
Phase 8 — Snowflake DWH Project (Sep 2026)
Phase 9 — Real Time Streaming (Oct 2026)
Phase 10 — dbt + Analytics (Nov 2026)
Phase 11 — Azure/GCP Project (Dec 2026)
Phase 12 — Interview Prep (Jan 2027)
Apply for jobs → Jan 2027! 🎉
```

---

## 👨‍💻 Author

**Phani Durga**
- GitHub: [@gpdurga06-collab](https://github.com/gpdurga06-collab)
- LinkedIn: [Add your LinkedIn URL here]
- Email: gpdurga06@gmail.com

---

*Built with ❤️ using AWS, Databricks, PySpark, Terraform, Docker and Kubernetes*

![GitHub last commit](https://img.shields.io/github/last-commit/gpdurga06-collab/ecommerce-data-platform)
![GitHub repo size](https://img.shields.io/github/repo-size/gpdurga06-collab/ecommerce-data-platform)
