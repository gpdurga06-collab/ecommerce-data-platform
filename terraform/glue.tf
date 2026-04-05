#glue catalog database
# The "aws_glue_catalog_database" resource creates a Glue Catalog Database, which serves as a logical container for tables in AWS Glue. It helps organize and manage metadata for your data stored in S3 or other data sources.


resource "aws_glue_catalog_database" "glue_catalog_database" {
  name        = "${var.project_name}_${var.environment}_catalog"
  description = "Glue Catalog Database for ${var.project_name} in ${var.environment} environment"

  tags = {
    Name        = "${var.project_name}-${var.environment}-glue-catalog-database"
    Environment = var.environment
    Project     = var.project_name

  }
}

#glue crawler pointing to raw s3 bucket, and storing in glue catalog database, using glue role
# The "aws_glue_crawler" resource creates a Glue Crawler that scans data in specified S3 buckets and populates the Glue Catalog Database with metadata about the data. The crawler uses the IAM role to access the data and perform its operations.

resource "aws_glue_crawler" "glue_crawler" {
  name          = "${var.project_name}-${var.environment}-crawler"
  database_name = aws_glue_catalog_database.glue_catalog_database.name
  role          = aws_iam_role.glue_role.arn


  s3_target {
    path = "s3://${aws_s3_bucket.raw.bucket}/"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-glue-crawler"
    Environment = var.environment
    Project     = var.project_name
  }
}

#glue job to process data from raw to curated, using glue role
# The "aws_glue_job" resource creates a Glue Job that defines the ETL (Extract, Transform, Load) process to move and transform data from the raw S3 bucket to the curated S3 bucket. The job uses the IAM role to access the data and perform its operations.

resource "aws_glue_job" "glue_job" {
  name     = "${var.project_name}-${var.environment}-glue-job"
  role_arn = aws_iam_role.glue_role.arn
  glue_version = "4.0"

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.raw.bucket}/scripts/glue_job_script.py"
    python_version  = "3"
  }

  worker_type       = "G.1X"
  number_of_workers = 2

  default_arguments = {
    "--job-language"   = "python"
    "--extra-py-files" = "s3://${aws_s3_bucket.raw.bucket}/scripts/dependencies.zip"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-glue-job"
    Environment = var.environment
    Project     = var.project_name
  }
}

