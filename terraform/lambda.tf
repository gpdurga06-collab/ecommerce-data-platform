resource "aws_lambda_function" "lambda_function" {
  filename      = "../ingestion/lambda/handler.zip"
  function_name = "${var.project_name}-${var.environment}-ingestion"
  role          =   aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "handler.lambda_handler"
  

  environment {
    variables = {
      ENVIRONMENT = var.environment
      BUCKET_NAME = aws_s3_bucket.raw.bucket
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-ingestion"
    Environment = var.environment
    Application = var.project_name
  }
}