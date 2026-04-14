
#glue role
# The "aws_iam_role" resource creates an IAM role that AWS Glue can assume to perform its operations.

resource "aws_iam_role" "glue_role" {
  name = "${var.project_name}-${var.environment}-glue-role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-glue-role"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "glue_role_policy_attachment" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_role_policy_attachment_s3" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

#lambda role
# The "aws_iam_role" resource creates an IAM role that AWS Lambda can assume to perform its operations.

resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-lambda-role"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "lambda_role_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_role_policy_attachment_s3" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

#EMR role
# The "aws_iam_role" resource creates an IAM role that Amazon EMR can assume

resource "aws_iam_role" "emr_role" {
  name = "${var.project_name}-${var.environment}-emr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-emr-role"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "emr_role_policy_attachment" {
  role       = aws_iam_role.emr_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

resource "aws_iam_role_policy_attachment" "emr_role_policy_attachment_s3" {
  role       = aws_iam_role.emr_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

#step function role
# The "aws_iam_role" resource creates an IAM role that AWS Step Functions can assume

resource "aws_iam_role" "step_function_role" {
  name = "${var.project_name}-${var.environment}-step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-step-function-role"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "step_function_role_policy_attachment" {
  role       = aws_iam_role.step_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSStepFunctionsFullAccess"
}

resource "aws_iam_role_policy_attachment" "step_function_role_policy_attachment_s3" {
  role       = aws_iam_role.step_function_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}


#AWS IAM Instance Profile for EMR
# The "aws_iam_instance_profile" resource creates an instance profile that can be associated with EC2 instances in the EMR cluster, allowing them to assume the EMR role and access necessary resources.

resource "aws_iam_instance_profile" "emr_instance_profile" {
  name = "${var.project_name}-${var.environment}-emr-instance-profile"
  role = aws_iam_role.emr_role.name
}

# role for Databricks connectivity
# The "aws_iam_role" resource creates an IAM role that can be assumed by Databricks to access AWS resources, such as S3 buckets, for data storage and processing. This role allows Databricks to interact with AWS services securely.
resource "aws_iam_role" "databricks_role" {
  name = "${var.project_name}-${var.environment}-databricks-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL"
        }
        Condition = {
          StringEquals = {
            "sts:ExternalId" = "d8d0bfa8-802c-4dcf-b489-e1baa957903a"
          }
        }
      },
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::978236789816:role/ecommerce-data-platform-dev-databricks-role"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-databricks-role"
    Environment = var.environment
    Project     = var.project_name
  }
}

# The "aws_iam_role_policy_attachment" resource attaches the AmazonS3FullAccess policy to the Databricks role, allowing it to access S3 buckets for data storage and retrieval.         
resource "aws_iam_role_policy_attachment" "databricks_role_policy_attachment_s3" {
  role       = aws_iam_role.databricks_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
