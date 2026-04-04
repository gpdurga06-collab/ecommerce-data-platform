resource "aws_s3_bucket" "raw" {
  bucket = "${var.project_name}-${var.environment}-raw"

  tags = {
    Name        = var.project_name
    Environment = var.environment
  }
}


# Versioning is separate resource
resource "aws_s3_bucket_versioning" "raw_versioning" {
  bucket = aws_s3_bucket.raw.id
  versioning_configuration {
    status = "Enabled"
  }
}




resource "aws_s3_bucket" "curated" {
  bucket = "${var.project_name}-${var.environment}-curated"

  tags = {
    Name        = var.project_name
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "curated_versioning" {
  bucket = aws_s3_bucket.curated.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "processed" {
  bucket = "${var.project_name}-${var.environment}-processed"

  tags = {
    Name        = var.project_name
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "processed_versioning" {
  bucket = aws_s3_bucket.processed.id
  versioning_configuration {
    status = "Enabled"
  }
}
