resource "aws_lambda_function" "lambda_function" {
  filename      = "../ingestion/lambda/handler.zip"
  function_name = "${var.project_name}-${var.environment}-ingestion"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "handler.lambda_handler"
  timeout       = 60

  environment {
    variables = {
      BUCKET_NAME       = aws_s3_bucket.raw.bucket
      STATE_MACHINE_ARN = aws_sfn_state_machine.pipeline.arn
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-ingestion"
    Environment = var.environment
    Application = var.project_name
  }
}