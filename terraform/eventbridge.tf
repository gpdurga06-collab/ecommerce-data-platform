#resource for eventbridge
# S3 notification → Lambda
resource "aws_s3_bucket_notification" "new_data" {
  bucket = aws_s3_bucket.raw.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.lambda_function.arn
    events = ["s3:ObjectCreated:*"]
    filter_prefix = "orders/"
  }
}

# Allow S3 to invoke Lambda
resource "aws_lambda_permission" "s3_invoke_lambda" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.raw.arn
}

# EventBridge scheduled rule
resource "aws_cloudwatch_event_rule" "daily_pipeline" {
  name                = "${var.project_name}-${var.environment}-daily-pipeline"
  description         = "Trigger pipeline every night at midnight"
  schedule_expression = "cron(0 0 * * ? *)"
}


# EventBridge target → Step Functions
resource "aws_cloudwatch_event_target" "step_functions_target" {
  rule     = aws_cloudwatch_event_rule.daily_pipeline.name
  arn      = aws_sfn_state_machine.pipeline.arn
  role_arn = aws_iam_role.step_function_role.arn
}